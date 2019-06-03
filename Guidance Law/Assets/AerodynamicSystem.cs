using UnityEngine;
using System.Collections;

public class AerodynamicSystem : MonoBehaviour 
{
    Rigidbody rb;

    public bool resetCOM = false;
    public Vector3 overrideCOM = Vector3.zero;

    public float referenceSurfaceArea = 1.5f;
    public float CLA = 0.25f;
    public float CD0 = 0.15f;
    public float CDL = 0.18f;
    public float wingMAC = 0.25f;
    public float wingCenter = -0.2f;

    public float maxCtrlSurfDeflection = 10f;
    public float ctrlSurfCLA = 0.95f;
    public float ctrlSurfCD0 = 0.02f;
    public float ctrlSurfCDL = 0.08f;
    public float ctrlSurfArea = 0.2f;
    public float ctrlSurfMAC = 0.1f;
    public float ctrlSurfCenter = -1.2f;
    public float ctrlSurfSpan = 0.15f;
    public float maxCtrlSurfDeflectRate = 320f;

    private float prevFramePitch = 0f;
    private float prevFrameYaw = 0f;
    private float prevFrameRoll = 0f;

    public bool showDebug = false;

    /// <summary>
    /// Returns the air density at given altitude.
    /// </summary>
    /// <param name="altitude">ASL in meter unit.</param>
    /// <returns>Air density in kg/m3 unit.</returns>
    public static float GetAirDensity(float altitude)
    {
        return 1.29f * Mathf.Pow(0.52f, altitude / 5000f);
    }

    public static float GetSoundSpeed(float altitude)
    {
        if(altitude > 11000)
            altitude = 11000;
        return 342f * (1f - altitude / 11000f * 0.125f);
    }

    public static float GetDynamicPressure(float altitude, float speed)
    {
        return 0.5f * GetAirDensity(altitude) * speed * speed;
    }

    public static float GetAeroCenter(float altitude, float speed, float MAC)
    {
        float mach = speed / GetSoundSpeed(altitude);
        if (mach < 0.85f)
        {
            return MAC * 0.25f;
        }
        else if (mach > 1.5f)
        {
            return MAC * 0.5f;
        }
        else if (mach < 1.0f)
        {
            return MAC * Mathf.Lerp(0.25f, 0.2f, (mach - 0.85f) / 0.15f);
        }
        else
        {
            return MAC * Mathf.Lerp(0.2f, 0.5f, (mach - 1f) / 0.5f);
        }
    }

	// Use this for initialization
	void Start () 
    {
        rb = this.GetComponent<Rigidbody>();
        if (resetCOM)
            rb.centerOfMass = overrideCOM;
    }
	
	// Update is called once per frame
	void FixedUpdate ()
    {
        float alpha = Vector3.Angle(this.transform.forward, rb.velocity);
        float coeffLift = 0f;
        float coeffDrag = 0f;

        float coeffLiftSign = 1;
        if (alpha > 90f)
        {
            alpha = 180f - alpha;
            coeffLiftSign = -1;
        }

        if (alpha < 30f)
        {
            coeffLift = alpha * CLA;
            coeffDrag = CD0 + coeffLift * coeffLift * CDL;
        }
        else
        {
            coeffLift = 30 * CLA * (30 / alpha);
            coeffDrag = CD0 + (alpha * CLA) * (alpha * CLA) * CDL;
        }

        coeffLift *= coeffLiftSign;

        float velocityMag = rb.velocity.magnitude;
        Vector3 liftDir = Vector3.Cross(Vector3.Cross(rb.velocity.normalized, this.transform.forward).normalized, rb.velocity.normalized).normalized;

        float aeroCenterOffset = GetAeroCenter(this.transform.position.y, velocityMag, wingMAC);
        Vector3 aeroCenter = new Vector3(0f, 0f, wingCenter - wingMAC * 0.5f + aeroCenterOffset);

        Vector3 lift = coeffLift * GetDynamicPressure(this.transform.position.y, velocityMag) * referenceSurfaceArea * liftDir;
        rb.AddForceAtPosition(lift, this.transform.TransformPoint(aeroCenter));
        Debug.DrawRay(this.transform.TransformPoint(aeroCenter), lift * 0.01f, Color.blue, 0.01f);

        Vector3 drag = coeffDrag * GetDynamicPressure(this.transform.position.y, velocityMag) * referenceSurfaceArea * (-rb.velocity.normalized);
        rb.AddForceAtPosition(drag, this.transform.TransformPoint(aeroCenter));
        Debug.DrawRay(this.transform.TransformPoint(aeroCenter), drag * 0.01f, Color.red, 0.01f);
	}

    public void SetupControlSurface(float pitch, float yaw, float roll)
    {
        if (showDebug)
            Debug.Log("CtrlInput: " + pitch.ToString("F2") + " " + yaw.ToString("F2") + " " + roll.ToString("F2"));
        
        float velocityMag = rb.velocity.magnitude;

        pitch = Mathf.Clamp(pitch, -maxCtrlSurfDeflection, maxCtrlSurfDeflection);
        yaw = Mathf.Clamp(yaw, -maxCtrlSurfDeflection, maxCtrlSurfDeflection);
        roll = Mathf.Clamp(roll, -maxCtrlSurfDeflection, maxCtrlSurfDeflection);

        float maxDeflectPerFrame = maxCtrlSurfDeflectRate * Time.fixedDeltaTime;
        pitch = Mathf.MoveTowards(prevFramePitch, pitch, maxDeflectPerFrame);
        yaw = Mathf.MoveTowards(prevFrameYaw, yaw, maxDeflectPerFrame);
        roll = Mathf.MoveTowards(prevFrameRoll, roll, maxDeflectPerFrame);

        prevFramePitch = pitch;
        prevFrameYaw = yaw;
        prevFrameRoll = roll;

        // Pitch.
        float coeffLift = pitch * ctrlSurfCLA;
        float coeffDrag = ctrlSurfCD0 + coeffLift * coeffLift * ctrlSurfCDL;

        Vector3 liftDir = this.transform.up * -1f;

        float aeroCenterOffset = GetAeroCenter(this.transform.position.y, velocityMag, ctrlSurfMAC);
        Vector3 aeroCenter = new Vector3(0f, 0f, ctrlSurfCenter - ctrlSurfMAC * 0.5f + aeroCenterOffset);
        
        Vector3 lift = coeffLift * GetDynamicPressure(this.transform.position.y, velocityMag) * ctrlSurfArea * liftDir;
        rb.AddForceAtPosition(lift, this.transform.TransformPoint(aeroCenter));
        Debug.DrawRay(this.transform.TransformPoint(aeroCenter), lift * 0.01f, Color.green, 0.01f);

        Vector3 drag = coeffDrag * GetDynamicPressure(this.transform.position.y, velocityMag) * ctrlSurfArea * (-rb.velocity.normalized);
        rb.AddForceAtPosition(drag, this.transform.TransformPoint(aeroCenter));
        Debug.DrawRay(this.transform.TransformPoint(aeroCenter), drag * 0.01f, Color.yellow, 0.01f);

        // Yaw.
        coeffLift = yaw * ctrlSurfCLA;
        coeffDrag = ctrlSurfCD0 + coeffLift * coeffLift * ctrlSurfCDL;

        liftDir = this.transform.right * -1f;

        aeroCenterOffset = GetAeroCenter(this.transform.position.y, velocityMag, ctrlSurfMAC);
        aeroCenter = new Vector3(0f, 0f, ctrlSurfCenter - ctrlSurfMAC * 0.5f + aeroCenterOffset);

        lift = coeffLift * GetDynamicPressure(this.transform.position.y, velocityMag) * ctrlSurfArea * liftDir;
        rb.AddForceAtPosition(lift, this.transform.TransformPoint(aeroCenter));
        Debug.DrawRay(this.transform.TransformPoint(aeroCenter), lift * 0.01f, Color.green, 0.01f);

        drag = coeffDrag * GetDynamicPressure(this.transform.position.y, velocityMag) * ctrlSurfArea * (-rb.velocity.normalized);
        rb.AddForceAtPosition(drag, this.transform.TransformPoint(aeroCenter));
        Debug.DrawRay(this.transform.TransformPoint(aeroCenter), drag * 0.01f, Color.yellow, 0.01f);

        // Roll.
        coeffLift = roll * ctrlSurfCLA;
        coeffDrag = ctrlSurfCD0 + coeffLift * coeffLift * ctrlSurfCDL;

        liftDir = this.transform.forward * ctrlSurfSpan;

        aeroCenterOffset = GetAeroCenter(this.transform.position.y, velocityMag, ctrlSurfMAC);
        aeroCenter = new Vector3(0f, 0f, ctrlSurfCenter - ctrlSurfMAC * 0.5f + aeroCenterOffset);

        lift = coeffLift * GetDynamicPressure(this.transform.position.y, velocityMag) * ctrlSurfArea * liftDir;
        lift *= 4f;
        rb.AddTorque(lift);
        Debug.DrawRay(this.transform.TransformPoint(aeroCenter), lift * 0.01f, Color.magenta, 0.01f);

        drag = coeffDrag * GetDynamicPressure(this.transform.position.y, velocityMag) * ctrlSurfArea * (-rb.velocity.normalized);
        rb.AddForceAtPosition(drag, this.transform.TransformPoint(aeroCenter));
        Debug.DrawRay(this.transform.TransformPoint(aeroCenter), drag * 0.01f, Color.yellow, 0.01f);

    }
}
