using UnityEngine;
using System.Collections;

public class ForceTeleport : MonoBehaviour {
    GameObject car;
    public Transform point1;
	// Use this for initialization
	void Start () {
        car = GameObject.Find("Car");
	}
	
	// Update is called once per frame
	void Update () {
	
	}

    void OnTriggerEnter(Collider collider)
    {
        if (collider.name.Contains("ColliderBody"))
        {
            car.transform.position = point1.position;
        }
    }
}
