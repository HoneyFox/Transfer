Shader "BHShader"
{
	Properties
	{
		_Gravity("Gravity", Float) = 1.0
		_Size("Size", Float) = 70
		_LightCurveness("LightCurveness", Float) = 70
		_Center("Center", Vector) = (0.0, 0.0, 0.0, 0.0)
	}

		SubShader
	{
		Tags
		{
			"RenderType" = "Transparent"
			"Queue" = "Transparent+1"
		}
		LOD 100

		// ------------------------------------------------------------------
		//  Base forward pass (directional light, emission, lightmaps, ...)
		Pass
		{
			Name "FORWARD"
			Tags { "LightMode" = "ForwardBase" }

			Blend SrcAlpha OneMinusSrcAlpha
			Cull Back
			ZWrite True
			ZTest LEqual
			Blend SrcAlpha OneMinusSrcAlpha

			CGPROGRAM
			#pragma target 3.0

			// -------------------------------------

			#pragma vertex vertBase
			#pragma fragment fragBase

			#include "UnityCG.cginc"
			
			float _Gravity;
			float _Size;
			float _LightCurveness;
			float4 _Center;

			struct appdata_t {
				float4 vertex : POSITION;
				float3 normal : NORMAL;
			};

			struct v2f {
				float4 vertex : SV_POSITION;
				float4 position : TEXCOORD0;
				float3 normal : NORMAL;
			};
			
			v2f vertBase(appdata_t v)
			{
				v2f o;
				o.position = mul(unity_ObjectToWorld, v.vertex);
				o.vertex = UnityObjectToClipPos(v.vertex);
				o.normal = normalize(mul(unity_ObjectToWorld, v.normal.xyz));
				return o;
			}

			float4 fragBase(v2f i) : COLOR
			{
				float3 camPos = _WorldSpaceCameraPos;
				float3 viewVector = normalize(i.position - camPos);
				float3 vecToCenter = _Center - i.position;
				float distanceToCenter = sqrt(1 - pow(dot(viewVector, normalize(vecToCenter)), 2)) * length(vecToCenter);
				if (distanceToCenter < _Gravity) {
					return float4(0, 0, 0, 1);
				}
				else {
					float gravCoeff = (distanceToCenter - _Gravity) / (_Size / 2 - _Gravity); // center - border: 0 - 1
					float angle = _LightCurveness * pow(1 - gravCoeff, 2);
					float3 vertAxis = cross(viewVector, normalize(vecToCenter));
					float3 pedalVector = normalize(cross(vertAxis, viewVector));
					float3 lightVector = normalize(cos(angle / 180 * 3.1415926) * viewVector + sin(angle / 180 * 3.1415926) * pedalVector);
					float4 reflect = UNITY_SAMPLE_TEXCUBE(unity_SpecCube0, lightVector);
					reflect.a = saturate(pow(dot(normalize(vecToCenter), viewVector) * 1.2, 4));
					return reflect;
				}
			}
            
            ENDCG
        }
    }
		
    FallBack "VertexLit"
}
