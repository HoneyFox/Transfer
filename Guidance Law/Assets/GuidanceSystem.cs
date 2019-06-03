using UnityEngine;
using System.Collections;

public class GuidanceSystem : MonoBehaviour 
{
    Rigidbody rb;
    AerodynamicSystem ads;
    FuzeSystem fz;

    private Vector3 prevFrameLOSVector;
    public float kNav = 3;
    public float initialLoftBias = 3f;
    public float cruiseLoftBias = 1f;
    public float loftTimer = 99999f;
    private float currentTime = 0f;
    public Vector3 injectVector;
    public float injectBias = 0.8f;
    public float pitchDamper = 0.1f;
    public float yawDamper = 0.1f;
    public float rollDamper = 0.1f;
    public float bankDamper = 0.1f;
    
    private Vector3 prevFramePosition;

    public bool showDebug = false;

	// Use this for initialization
	void Start () 
    {
        rb = this.GetComponent<Rigidbody>();
        ads = this.GetComponent<AerodynamicSystem>();
        fz = this.GetComponent<FuzeSystem>();

        if(rb != null)
            rb.velocity = this.transform.forward * 280f;

        injectVector = new Vector3(Random.Range(-10f, 10f), -8f, Random.Range(-10f, 10f));
	}
	
	// Update is called once per frame
	void FixedUpdate () 
    {
        currentTime += Time.fixedDeltaTime;

        if(prevFramePosition != Vector3.zero && (fz == null || fz.hasTriggered == false))
            Debug.DrawLine(prevFramePosition, transform.position, Color.cyan, 99999f);
        prevFramePosition = this.transform.position;

        Vector3 LOSVector = Vector3.zero - this.transform.position;
        if (prevFrameLOSVector.magnitude > 0f && rb != null)
        {
            Vector3 axis = Vector3.Cross(prevFrameLOSVector, LOSVector).normalized;
            float LOSRate = Vector3.Angle(prevFrameLOSVector, LOSVector) / Time.fixedDeltaTime;
            if (showDebug)
                Debug.Log(axis.ToString() + " " + LOSRate.ToString("F2"));

            Vector3 kNavAxis = axis * Mathf.Min(LOSRate, 2.5f) * kNav;
            Vector3 loftAxis = Vector3.Cross(new Vector3(0f, -1f, 0f), rb.velocity).normalized;
            Vector3 injectAxis = Vector3.Cross(injectVector.normalized, LOSVector.normalized);
            float offBoresightCoeff = Vector3.Dot(LOSVector.normalized, rb.velocity.normalized);

            float currentLoftBias = GetLoftBias();
            Vector3 turnAxis = kNavAxis + injectAxis * injectBias * offBoresightCoeff + loftAxis * currentLoftBias * Mathf.Sqrt((1 - Mathf.Pow(Vector3.Dot(rb.velocity.normalized, Vector3.up), 2f)));
            Debug.DrawRay(this.transform.position, kNavAxis);
            Debug.DrawRay(this.transform.position, loftAxis * currentLoftBias, Color.black);

            Vector3 localTurnAxis = this.transform.InverseTransformVector(turnAxis);
            Vector3 localAngularVelocity = this.transform.InverseTransformVector(rb.angularVelocity);

            float bankAngle = 0f;
            if (bankDamper != 0f)
            {
                Vector3 localUpVec = Vector3.Cross(Vector3.Cross(this.transform.forward, Vector3.up), this.transform.forward);
                bankAngle = Vector3.Angle(localUpVec, this.transform.up);
                float bankSide = Mathf.Sign(Vector3.Dot(localUpVec.normalized, this.transform.right));
                bankAngle *= bankSide;
                if (showDebug)
                    Debug.Log("Bank: " + bankAngle.ToString("F2"));
            }

            // Dynamic Pressure Adjustment
            float dynamicPressure = rb.velocity.sqrMagnitude * 0.5f * 1.29f;
            if (showDebug)
                Debug.Log("DynPrs: " + dynamicPressure.ToString("F2"));
            float adjustment = Mathf.Clamp(5000f / dynamicPressure, 0.2f, 1f);
            if (LOSVector.magnitude > 2000f) adjustment = 1f;
            else adjustment = Mathf.Lerp(1f, adjustment, 1f - LOSVector.magnitude / 2000f);

            // Apply forces by using control surfaces.
            ads.SetupControlSurface(
                (-localTurnAxis.x + localAngularVelocity.x * pitchDamper) * adjustment,
                (localTurnAxis.y + localAngularVelocity.y * -yawDamper) * adjustment,
                (localAngularVelocity.z + bankAngle * bankDamper)* -rollDamper * adjustment
            );
        }

        prevFrameLOSVector = LOSVector;
	}

    private float GetLoftBias()
    {
        if (currentTime >= loftTimer)
            return cruiseLoftBias;
        else
            return initialLoftBias;
    }
}
