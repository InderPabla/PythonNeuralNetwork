using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class CancerDetector : MonoBehaviour {
    public InputField thicknessField;
    public InputField sizeField;
    public InputField shapeField;
    public InputField adhesionField;
    public InputField epiField;
    public InputField bareField;
    public InputField blandField;
    public InputField normalField;
    public InputField mitosesField;

    private string retrievePage = "http://localhost:8000/BreastCancerResult/index.php?";
    private bool done = false;
    private WWW web = null;

    // Use this for initialization
    void Start ()
    {
	
	}
	
	// Update is called once per frame
	void Update ()
    {
	
	}

    public void OnCheckButtonPress()
    {
        if (!thicknessField.text.Equals("") && IsDigitsOnly(thicknessField.text) &&
            !sizeField.text.Equals("") && IsDigitsOnly(sizeField.text) &&
            !shapeField.text.Equals("") && IsDigitsOnly(shapeField.text) &&
            !adhesionField.text.Equals("") && IsDigitsOnly(adhesionField.text) &&
            !epiField.text.Equals("") && IsDigitsOnly(epiField.text) &&
            !bareField.text.Equals("") && IsDigitsOnly(bareField.text) &&
            !blandField.text.Equals("") && IsDigitsOnly(blandField.text) &&
            !normalField.text.Equals("") && IsDigitsOnly(normalField.text) &&
            !mitosesField.text.Equals("") && IsDigitsOnly(mitosesField.text))
        {

            StartCoroutine(GetResult());
        }
    }

    public IEnumerator GetResult()
    {
        string page = retrievePage; //retrieve page

        page +=
            "thickness=" + thicknessField.text +
            "&size=" + sizeField.text +
            "&shape=" + shapeField.text +
            "&adhesion=" + adhesionField.text +
            "&epi=" + epiField.text +
            "&bare=" + bareField.text +
            "&bland=" + blandField.text +
            "&normal=" + normalField.text +
            "&mitoses=" + mitosesField.text;  

        done = false; //set to fasle to wait for web to return

        web = new WWW(page); //run page
        yield return web; //wait for web to execute url
        
        Debug.Log(web.text);

        done = true; //retrieved is true
    }

    bool IsDigitsOnly(string str)
    {
        foreach (char c in str)
        {
            if (c < '0' || c > '9')
                return false;
        }

        return true;
    }
}
