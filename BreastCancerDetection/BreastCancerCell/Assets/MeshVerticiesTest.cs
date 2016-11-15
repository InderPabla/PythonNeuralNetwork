using UnityEngine;
using System.Collections;

public class MeshVerticiesTest : MonoBehaviour {

	// Use this for initialization
	void Start () {
        Mesh mesh = GetComponent<MeshFilter>().mesh;
        Vector3[] verts = mesh.vertices;

        verts[0] += new Vector3(-0.1f,0, -0.1f);
        mesh.vertices = verts;
    }
	
	// Update is called once per frame
	void Update () {
	
	}
}
