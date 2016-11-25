using UnityEngine;
using System.Collections;

public class ColorChanger : MonoBehaviour {
    HSBColor color = new HSBColor(0f,1f,1f);
	// Use this for initialization
	void Start () {
	    
	}
	
	// Update is called once per frame
	void Update () {
        GetComponent<Renderer>().sharedMaterials[0].color = color.ToColor();
        color.h += 0.0005f;
        if (color.h >= 1f)
            color.h = 0f;

        if (color.h > 0.38f && color.h < 0.7f)
            color.h = 0.7f;
    }
}
