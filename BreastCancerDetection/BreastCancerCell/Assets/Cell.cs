using UnityEngine;
using System.Collections;

public class Cell : MonoBehaviour {

    public GameObject cellPrefab;


    CancerData data;
    // Use this for initialization
    public void Activate(CancerData data) {
        this.data = data;
        
        GetComponent<Rigidbody2D>().velocity = new Vector2(Random.Range(-0.5f * (data.adhesion / 10f), 0.5f * (data.adhesion / 10f)), 
                                                           Random.Range(-0.5f * (data.adhesion / 10f), 0.5f * (data.adhesion / 10f)));
        GetComponent<Rigidbody2D>().drag = (1f - (data.adhesion / 10f)) +0.2f;
        GetComponent<Rigidbody2D>().angularDrag = (1f - (data.adhesion / 10f)) + 0.2f;
        PhysicsMaterial2D material = new PhysicsMaterial2D();

        material.friction = 1f-(data.adhesion /10f);
        material.bounciness = data.adhesion / 10f;
        GetComponent<CircleCollider2D>().sharedMaterial = material;

        //Debug.Log(mitoses);
        float shapeFactor = (data.shape / 20f);

        float width = UnityEngine.Random.Range(0.5f, 0.5f + shapeFactor);
        float height = UnityEngine.Random.Range(0.5f, 0.5f + shapeFactor);

        float sizeFactor = data.size /15f;
        float nucleasSizeFactor = data.bland / 2f;

        float minSize = 0f;
        if (width > height)
        {

            float sizeX = 0.5f * (sizeFactor + 1f);
            float sizeY = 0.5f * (height / width) * (sizeFactor + 1f);

            transform.localScale = new Vector3(UnityEngine.Random.Range(0.5f,sizeX), UnityEngine.Random.Range(0.5f, sizeY), 0.01f);
            minSize = height;
            transform.GetComponent<CircleCollider2D>().radius = (0.533f - (0.1f * (data.epi / 10f))) * (height / width);

            
        }
        else
        {
            float sizeX = 0.5f * (width / height) * (sizeFactor + 1f);
            float sizeY = 0.5f * (sizeFactor + 1f);

            transform.localScale = new Vector3(UnityEngine.Random.Range(0.5f, sizeX), UnityEngine.Random.Range(0.5f, sizeY), 0.01f);

            
            minSize = width;
            transform.GetComponent<CircleCollider2D>().radius = (0.533f -(0.1f*(data.epi / 10f))) * (width/height);
        }

        float fixedRatio = 0.5f / 0.066f;

        float newXSize =  transform.localScale.x/ fixedRatio;
        float newYSize =  transform.localScale.y / fixedRatio;
        //Debug.Log(newXSize + " " + fixedRatio + " " + transform.localScale.x);
        transform.GetChild(0).localScale = new Vector3(newXSize * (nucleasSizeFactor + 1f), newYSize * (nucleasSizeFactor + 1f), 0.01f);

        Color color = Color.green;
        float highestAlpha = 0.8f;
        float alphaRatio = data.bare / 10f;
        float newAlpha = highestAlpha * (1f-alphaRatio);
        color.a = UnityEngine.Random.Range(newAlpha/2f, newAlpha*1.1f);
        if (color.a > newAlpha)
            color.a = newAlpha;

        transform.GetChild(1).GetComponent<Renderer>().material.color = color;
        transform.GetChild(1).GetComponent<Renderer>().material.shader = Shader.Find("Transparent/Diffuse");

        color = Color.white;
        color.a = UnityEngine.Random.Range(0f, data.normal /10f);
        transform.GetChild(2).GetComponent<Renderer>().material.color = color;
        transform.GetChild(2).GetComponent<Renderer>().material.shader = Shader.Find("Transparent/Diffuse");
        /*Vector3 position = transform.position;
        float y = 0f;
        float probablityOfChange = UnityEngine.Random.Range(0f, epi / 10f);
        float realProb = UnityEngine.Random.Range(0f, 1f);

        if (probablityOfChange > realProb)
        {
            //realProb = UnityEngine.Random.Range(0f, 1f);
            //if (probablityOfChange > realProb)
            //{
                y = UnityEngine.Random.Range(0, 2);
                if (y == 0)
                    y = -(transform.localScale.y+0.05f);
                else
                    y = (transform.localScale.y + 0.05f);
                Debug.Log("AAAA");
            y += UnityEngine.Random.Range(-0.01f*(epi/10f),0.01f * (epi / 10f));
            //}

        }

        position += new Vector3(UnityEngine.Random.Range(-0.5f, 0.5f), y, 0f);
        transform.position = position;*/
        transform.position += new Vector3(UnityEngine.Random.Range(-0.1f, 0.1f), UnityEngine.Random.Range(-0.1f, 0.1f), 0f);

        if (data.mitoses > 0)
        {
            Invoke("Reproduce", UnityEngine.Random.Range(0f,0.5f));
        }    
    }

    void Reproduce()
    {
        for (int i = 0; i < data.mitoses /4; i++)
        {
            Invoke("GrowCell", (float)i*0.25f + 0.25f);
        }

    }

    void GrowCell()
    {
        int random = UnityEngine.Random.Range(0, (int)data.mitoses + 1);
        /*Vector3 position = new Vector3(UnityEngine.Random.Range(transform.position.x - 0.001f, transform.position.x + 0.001f),
                                        UnityEngine.Random.Range(transform.position.y - 0.001f, transform.position.y + 0.001f),
                                        UnityEngine.Random.Range(0, (int)thickness/5));*/

        Vector3 position = new Vector3(transform.position.x, transform.position.y, UnityEngine.Random.Range(0, (int)data.thickness));
        
        if (random > 0)
        {
            GameObject obj = (GameObject)Instantiate(cellPrefab, position, cellPrefab.transform.rotation);
            /*obj.GetComponent<Cell>().mitoses = mitoses-1.5f;
            if (obj.GetComponent<Cell>().mitoses < 0f)
                obj.GetComponent<Cell>().mitoses = 0f;*/
            
            obj.transform.eulerAngles = new Vector3(0,0,UnityEngine.Random.Range(0f,360f));
            CancerData newData = new CancerData(data);
            newData.mitoses -= 1f;
            obj.SendMessage("Activate",newData);
            obj.transform.parent = transform.parent;
        }
    }

    /*public void SetMitoses(object mitoses)
    {
        this.mitoses = (float)mitoses;
    }*/

	// Update is called once per frame
	void Update () {
	    
	}


}
