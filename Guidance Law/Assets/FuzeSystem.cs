using UnityEngine;
using System.Collections;

public class FuzeSystem : MonoBehaviour
{
    public Transform tfFuze;
    public float fuzeDistance;
    public bool hasTriggered = false;

	// Use this for initialization
	void Start () 
    {
	    
	}
	
	// Update is called once per frame
	void FixedUpdate () 
    {
        if (hasTriggered) return;

        RaycastHit hitInfo;
	    if(Physics.Raycast(new Ray(tfFuze.position, tfFuze.forward), out hitInfo, fuzeDistance))
        {
            Debug.DrawRay(hitInfo.point, tfFuze.forward * fuzeDistance, Color.red, 9999f, false);
            hasTriggered = true;
        }
	}
}
