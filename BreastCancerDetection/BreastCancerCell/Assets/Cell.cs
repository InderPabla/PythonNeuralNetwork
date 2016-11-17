using UnityEngine;
using System.Collections;

public class Cell : MonoBehaviour {

    public GameObject cellPrefab;

    float thickness = 5; 
    float size = 2;
    float shape = 1;
    float adhesion = 10;
    float epi = 0;
    float bare = 10;
    float bland = 1;
    float normal = 0;
    float mitoses = 10;

    // Use this for initialization
    void Start() {

        GetComponent<Rigidbody2D>().velocity = new Vector2(Random.Range(-0.5f * (adhesion / 10f), 0.5f * (adhesion / 10f)), 
                                                           Random.Range(-0.5f * (adhesion / 10f), 0.5f * (adhesion / 10f)));
        GetComponent<Rigidbody2D>().drag = (1f - (adhesion / 10f)) +0.2f;
        GetComponent<Rigidbody2D>().angularDrag = (1f - (adhesion / 10f)) + 0.2f;
        PhysicsMaterial2D material = new PhysicsMaterial2D();

        material.friction = 1f-(adhesion/10f);
        material.bounciness = adhesion / 10f;
        GetComponent<CircleCollider2D>().sharedMaterial = material;

        Debug.Log(mitoses);
        float shapeFactor = (shape / 20f);

        float width = UnityEngine.Random.Range(0.5f, 0.5f + shapeFactor);
        float height = UnityEngine.Random.Range(0.5f, 0.5f + shapeFactor);

        float sizeFactor = size /15f;
        float nucleasSizeFactor = bare / 2f;

        float minSize = 0f;
        if (width > height)
        {

            float sizeX = 0.5f * (sizeFactor + 1f);
            float sizeY = 0.5f * (height / width) * (sizeFactor + 1f);

            transform.localScale = new Vector3(UnityEngine.Random.Range(0.5f,sizeX), UnityEngine.Random.Range(0.5f, sizeY), 0.01f);
            minSize = height;
            transform.GetComponent<CircleCollider2D>().radius = (0.533f - (0.1f * (thickness / 10f))) * (height / width);

            
        }
        else
        {
            float sizeX = 0.5f * (width / height) * (sizeFactor + 1f);
            float sizeY = 0.5f * (sizeFactor + 1f);

            transform.localScale = new Vector3(UnityEngine.Random.Range(0.5f, sizeX), UnityEngine.Random.Range(0.5f, sizeY), 0.01f);

            
            minSize = width;
            transform.GetComponent<CircleCollider2D>().radius = (0.533f -(0.1f*(thickness/10f))) * (width/height);
        }

        float fixedRatio = 0.5f / 0.066f;

        float newXSize =  transform.localScale.x/ fixedRatio;
        float newYSize =  transform.localScale.y / fixedRatio;
        Debug.Log(newXSize + " " + fixedRatio + " " + transform.localScale.x);
        transform.GetChild(0).localScale = new Vector3(newXSize * (nucleasSizeFactor + 1f), newYSize * (nucleasSizeFactor + 1f), 0.01f);

        float highestAlpha = 0.75f;
        float highestRemoveAlpha = 0.5f;
        float alphaRatio = bland / 10f;
        float newAlpha = highestRemoveAlpha * (1f - alphaRatio);
        Color color = Color.red;

        color.a = UnityEngine.Random.Range(0f, highestAlpha- highestRemoveAlpha);
        
        transform.GetChild(1).GetComponent<Renderer>().material.color = color;
        transform.GetChild(1).GetComponent<Renderer>().material.shader = Shader.Find("Transparent/Diffuse");


        if (mitoses > 0)
        {
            Invoke("Reproduce", (float)0f);
        }    
    }

    void Reproduce()
    {
        for (int i = 0; i < mitoses/5; i++)
        {
            Invoke("GrowCell", (float)i*0.25f + 0.25f);
        }

    }

    void GrowCell()
    {
        int random = UnityEngine.Random.Range(0, (int)mitoses + 1);
        /*Vector3 position = new Vector3(UnityEngine.Random.Range(transform.position.x - 0.001f, transform.position.x + 0.001f),
                                        UnityEngine.Random.Range(transform.position.y - 0.001f, transform.position.y + 0.001f),
                                        UnityEngine.Random.Range(0, (int)thickness/5));*/

        Vector3 position = new Vector3(transform.position.x, transform.position.y, UnityEngine.Random.Range(0, (int)thickness));
        position += new Vector3(UnityEngine.Random.Range(-0.1f,0.1f), UnityEngine.Random.Range(-0.1f, 0.1f),0f);
        if (random > 0)
        {
            GameObject obj = (GameObject)Instantiate(cellPrefab, position, cellPrefab.transform.rotation);
            obj.GetComponent<Cell>().mitoses = mitoses-1;
            if (obj.GetComponent<Cell>().mitoses < 0f)
                obj.GetComponent<Cell>().mitoses = 0f;
            obj.transform.eulerAngles = new Vector3(0,0,UnityEngine.Random.Range(0f,360f));
        }
    }

    public void SetMitoses(object mitoses)
    {
        this.mitoses = (float)mitoses;
    }

	// Update is called once per frame
	void Update () {
	    
	}


}
