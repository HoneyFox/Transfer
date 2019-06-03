using UnityEngine;
using System.Collections;

public class PropulsionSystem : MonoBehaviour
{
    Rigidbody rb;

    public float boosterTime = 5f;
    public float boosterThrust = 2000f;
    public float sustainerTime = 0f;
    public float sustainerThrust = 220f;

    public float boosterPropellantMass = 20f;
    public float sustainerPropellantMass = 20f;

    private float currentTime = 0f;

    public Transform separateBooster;
    public Vector3 separateVelocity;
    public float boosterMass;

	// Use this for initialization
	void Start ()
    {
        rb = this.GetComponent<Rigidbody>();
	}
	
	// Update is called once per frame
	void FixedUpdate () 
    {
        currentTime += Time.fixedDeltaTime;
        if(currentTime < boosterTime)
        {
            rb.AddRelativeForce(new Vector3(0f, 0f, boosterThrust));
            rb.mass -= boosterPropellantMass * (Time.fixedDeltaTime / boosterTime);
        }
        else if (currentTime < boosterTime + sustainerTime)
        {
            rb.AddRelativeForce(new Vector3(0f, 0f, sustainerThrust));
            rb.mass -= sustainerPropellantMass * (Time.fixedDeltaTime / sustainerTime);
        }
        else
        {
            // No thrust here.
            if (separateBooster != null)
            {
                separateBooster.SetParent(this.transform.parent);
                Rigidbody boosterRb = separateBooster.gameObject.AddComponent<Rigidbody>();
                boosterRb.mass = boosterMass;
                boosterRb.velocity = rb.velocity + this.transform.TransformVector(separateVelocity);
                separateBooster.GetComponent<AerodynamicSystem>().enabled = true;
                separateBooster = null;
                rb.mass -= boosterMass;
            }
        }
	}

    void OnGUI()
    {
        GUILayout.BeginArea(new Rect(0f, 0f, 500f, 500f));
        GUILayout.Label("Time: " + currentTime.ToString("F2"));
        GUILayout.Label("Speed: " + rb.velocity.magnitude.ToString("F0"));
        GUILayout.EndArea();
    }
}
