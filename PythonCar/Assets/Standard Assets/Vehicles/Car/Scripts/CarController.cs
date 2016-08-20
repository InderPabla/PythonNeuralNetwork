using System;
using UnityEngine;
using System.IO;
using System.Threading;
using System.Security.Permissions;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System.Collections.Generic;

namespace UnityStandardAssets.Vehicles.Car
{
    internal enum CarDriveType
    {
        FrontWheelDrive,
        RearWheelDrive,
        FourWheelDrive
    }

    internal enum SpeedType
    {
        MPH,
        KPH
    }

    public class CarController : MonoBehaviour
    {
        [SerializeField]
        private CarDriveType m_CarDriveType = CarDriveType.FourWheelDrive;
        [SerializeField]
        private WheelCollider[] m_WheelColliders = new WheelCollider[4];
        [SerializeField]
        private GameObject[] m_WheelMeshes = new GameObject[4];
        [SerializeField]
        private WheelEffects[] m_WheelEffects = new WheelEffects[4];
        [SerializeField]
        private Vector3 m_CentreOfMassOffset;
        [SerializeField]
        private float m_MaximumSteerAngle;
        [Range(0, 1)]
        [SerializeField]
        private float m_SteerHelper; // 0 is raw physics , 1 the car will grip in the direction it is facing
        [Range(0, 1)]
        [SerializeField]
        private float m_TractionControl; // 0 is no traction control, 1 is full interference
        [SerializeField]
        private float m_FullTorqueOverAllWheels;
        [SerializeField]
        private float m_ReverseTorque;
        [SerializeField]
        private float m_MaxHandbrakeTorque;
        [SerializeField]
        private float m_Downforce = 100f;
        [SerializeField]
        private SpeedType m_SpeedType;
        [SerializeField]
        private float m_Topspeed = 200;
        [SerializeField]
        private static int NoOfGears = 5;
        [SerializeField]
        private float m_RevRangeBoundary = 1f;
        [SerializeField]
        private float m_SlipLimit;
        [SerializeField]
        private float m_BrakeTorque;

        private Quaternion[] m_WheelMeshLocalRotations;
        private Vector3 m_Prevpos, m_Pos;
        private float m_SteerAngle;
        private int m_GearNum;
        private float m_GearFactor;
        private float m_OldRotation;
        private float m_CurrentTorque;
        private Rigidbody m_Rigidbody;
        private const float k_ReversingThreshold = 0.01f;

        public bool Skidding { get; private set; }
        public float BrakeInput { get; private set; }
        public float CurrentSteerAngle { get { return m_SteerAngle; } }
        public float CurrentSpeed { get { return m_Rigidbody.velocity.magnitude * 2.23693629f; } }
        public float MaxSpeed { get { return m_Topspeed; } }
        public float Revs { get; private set; }
        public float AccelInput { get; private set; }



        // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MY CODE STARTS HERE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MY CODE STARTS HERE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MY CODE STARTS HERE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        string raw_data_file = "C:\\Users\\Pabla\\Desktop\\ImageAnalysis\\AdvancedCarModel\\Data15\\raw_data.txt";
        string picture_location = "C:\\Users\\Pabla\\Desktop\\ImageAnalysis\\AdvancedCarModel\\Data15";
        string real_time_image = "C:\\Users\\Pabla\\Desktop\\ImageAnalysis\\AdvancedCarModel\\real_time.png";

        Camera camera;
        int resWidth = 50;
        int resHeight = 50;
        int filenumber = 0;
        bool collectInformaiton = false;
        FileStream file_stream;
        StreamWriter stream_writer;
        float turn = 0;
        float forward = 0;
        bool initComplete = false;
        Thread thread;
        TcpListener serverSocket;
        TcpClient acceptSocket;
        IPAddress address;
        byte[] imageBytes;
        bool isCaptured = true;
        float angularVelocity = 0;
        float velocity = 0;
        float outTurning = 0;
        float outForward = 0;
        NetworkStream stream;
        bool realTimeTraningMode = false;
        bool dataCollectMode = false;
        float recordSpeed = 0.1f;
        float signal = 0;
        float signalChangeTime = 5f;
        public TextMesh leftText;
        public TextMesh stayText;
        public TextMesh rightText;

        public void FixedUpdate()
        {
            if (initComplete == true && Input.GetKeyDown(KeyCode.P))
            {
                collectInformaiton = !collectInformaiton;
                if (collectInformaiton == false)
                {
                    stream_writer.Flush();
                    file_stream.Close();
                    stream_writer.Close();
                }
            }

            if (isCaptured == false)
            {
                angularVelocity = m_Rigidbody.angularVelocity.y;
                velocity = m_Rigidbody.velocity.magnitude;
                CaptureImage();

                isCaptured = true;


            }

            if (initComplete == false && realTimeTraningMode == false)
            {
                Move(outTurning, outForward, outForward, 0f);
            }

            //Debug.Log(m_Rigidbody.velocity.magnitude / 10f);
        }

        public void SignalChange() {
            float randomSignal = UnityEngine.Random.Range(0,2);

            /*if (signal == -1) {
                if (randomSignal == 0) {
                    signal = 0;
                }
                else if (randomSignal == 1) {
                    signal = 1;
                }
            }
            else if (signal == 0)
            {
                if (randomSignal == 0)
                {
                    signal = -1;
                }
                else if (randomSignal == 1)
                {
                    signal = 1;
                }
            }
            else if (signal == 1)
            {
                if (randomSignal == 0)
                {
                    signal = 0;
                }
                else if (randomSignal == 1)
                {
                    signal = -1;
                }
            }*/


            signal *=-1;
            leftText.text = "";
            stayText.text = "";
            rightText.text = "";

            if (signal == -1)
                leftText.text = "===";
            else if(signal == 1)
                rightText.text = "===";
            else
                stayText.text = "===";

            Invoke("SignalChange", signalChangeTime);
        }

        public void InitilizeDataCollection()
        {
            Invoke("PicTimer", 0.1f);
            file_stream = File.Create(raw_data_file);
            stream_writer = new StreamWriter(file_stream);
            initComplete = true;
        }

        public void PicTimer()
        {
            if (collectInformaiton == true)
            {
                TakePicture();
            }
            Invoke("PicTimer", recordSpeed);
        }

        public void CaptureImage()
        {

            /*RenderTexture rt = new RenderTexture(Screen.width, Screen.height, 24);
            camera.targetTexture = rt;
            Texture2D screenShot = new Texture2D(300, 300, TextureFormat.RGB24, false);
            camera.Render();
            RenderTexture.active = rt;
            screenShot.ReadPixels(new Rect((Screen.width / 2) - 150, (Screen.height / 2) - 195, 300, 300), 0, 0);*/

            /*RenderTexture rt = new RenderTexture(Screen.width, Screen.height, 24);
            camera.targetTexture = rt;
            Texture2D screenShot = new Texture2D(200, 200, TextureFormat.RGB24, false);
            camera.Render();
            RenderTexture.active = rt;
            screenShot.ReadPixels(new Rect((Screen.width / 2) - 100, (Screen.height / 2) - 130, 200, 200), 0, 0);*/

            RenderTexture rt = new RenderTexture(Screen.width, Screen.height, 24);
            camera.targetTexture = rt;
            Texture2D screenShot = new Texture2D(300, 300, TextureFormat.RGB24, false);
            camera.Render();
            RenderTexture.active = rt;
            screenShot.ReadPixels(new Rect((Screen.width / 2) - 150, (Screen.height / 2) - 100, 300, 300), 0, 0);
            screenShot = ScaleTexture(screenShot, 50, 50);

            screenShot = ScaleTexture(screenShot, 50, 50);
            camera.targetTexture = null;
            RenderTexture.active = null;
            Destroy(rt);

            byte[] bytes = /*screenShot.GetRawTextureData();*/screenShot.EncodeToPNG();
            System.IO.File.WriteAllBytes(real_time_image, bytes);
            //return bytes;
        }

        public void TakePicture()
        {
            RenderTexture rt = new RenderTexture(Screen.width, Screen.height, 24);
            camera.targetTexture = rt;
            Texture2D screenShot = new Texture2D(300, 300, TextureFormat.RGB24, false);
            camera.Render();
            RenderTexture.active = rt;
            screenShot.ReadPixels(new Rect((Screen.width / 2) - 150, (Screen.height / 2) - 100, 300, 300), 0, 0);
            screenShot = ScaleTexture(screenShot, 50, 50); 

            camera.targetTexture = null;
            RenderTexture.active = null;
            Destroy(rt);
            byte[] bytes = screenShot.EncodeToPNG();
            string filename = picture_location + "\\" + filenumber + ".png";

            System.IO.File.WriteAllBytes(filename, bytes);

            Vector3 angular_velo = m_Rigidbody.angularVelocity;
            Vector3 velo = m_Rigidbody.velocity;
            //Debug.Log(angular_velo.y + " " + velo.sqrMagnitude + " " + m_SteerAngle);

            //stream_writer.WriteLine(angular_velo.y + " " + (velo.sqrMagnitude/100f) + " " /*+ (m_SteerAngle) + " "*/ /*+ forward + " "*/ + turn);
            float one = 0;
            float two = 0;
            float three = 0;

            if (turn == -1f)
                one = 1f;
            else if (turn == 0f)
                two = 1f;
            else if (turn == 1f)
                three = 1f;


            stream_writer.WriteLine((velo.magnitude / 10f) + " " + one + " " + two + " " + three);
            //Debug.Log(angular_velo.y + " " + (velo.sqrMagnitude/100f) + " " /*+ (m_SteerAngle) + " "*/ /*+ forward + " "*/ + turn);
            filenumber++;
        }

        private Texture2D ScaleTexture(Texture2D source, int targetWidth, int targetHeight)
        {
            Texture2D result = new Texture2D(targetWidth, targetHeight, source.format, false);
            float incX = (1.0f / (float)targetWidth);
            float incY = (1.0f / (float)targetHeight);
            for (int i = 0; i < result.height; ++i)
            {
                for (int j = 0; j < result.width; ++j)
                {
                    Color newColor = source.GetPixelBilinear((float)j / (float)result.width, (float)i / (float)result.height);
                    result.SetPixel(j, i, newColor);
                }
            }
            result.Apply();
            return result;
        }

        public void Worker()
        {
            address = Dns.GetHostEntry("localhost").AddressList[0];
            serverSocket = new TcpListener(address, 12345);
            serverSocket.Start();

            acceptSocket = serverSocket.AcceptTcpClient();
            stream = acceptSocket.GetStream();
            Debug.Log("Connected");

            while (true)
            {

                isCaptured = false;
                while (isCaptured == false)
                {
                    //wait
                }


                int dataSize = 5;
                if (realTimeTraningMode == false)
                    dataSize = 2;

                float[] data = new float[dataSize];

                data[0] = signal;//angularVelocity;
                data[1] = velocity / 10f; //velocity = ((m_Rigidbody.velocity.sqrMagnitude/500f)*5f);
                //data[2] = m_SteerAngle;//(m_SteerAngle/15f); // /15

                if (realTimeTraningMode == true)
                {
                    data[3] = forward;
                    data[4] = turn;
                }

                byte[] convertedData = new byte[4 * data.Length];
                Buffer.BlockCopy(data, 0, convertedData, 0, convertedData.Length);
                stream.Write(convertedData, 0, convertedData.Length);

                byte[] bytes = new byte[256];

                stream.Read(bytes, 0, bytes.Length);
                string mstrMessage = Encoding.ASCII.GetString(bytes, 0, bytes.Length);

                double[] doubles = Array.ConvertAll(mstrMessage.Split(' '), new Converter<string, double>(Double.Parse));

                outTurning = (float)doubles[0];
                outForward = 1f;
                //Debug.Log(outForward+" "+outTurning);
            }
        }


        public void InitilizeWork()
        {
            Application.runInBackground = true;
            camera = Camera.main;

            signal = 1f;
            leftText.text = "";
            stayText.text = "";
            rightText.text = "";

            if (signal == -1)
                leftText.text = "===";
            else if (signal == 1)
                rightText.text = "===";

            Invoke("SignalChange", 500000000000f);

            if (dataCollectMode == true)
            {
                InitilizeDataCollection();   //<< NEEDS TO BE CALLED TO START TAKING PICTURES
            }
            else
            {
                thread = new Thread(Worker);
                thread.IsBackground = true; //not a dameon thread, must run in foreground
                thread.Start();
            }
        }

        void OnApplicationQuit()
        {
            if (thread.IsAlive)
            {
                try
                {
                    serverSocket.Stop();
                    stream.Close();
                    acceptSocket.Close();
                }
                catch (SocketException error)
                {
                    Debug.Log(error);
                }

                try
                {
                    KillTheThread();
                    Debug.Log(thread.IsAlive); //true (must be false)
                }
                catch (Exception error)
                {
                    Debug.Log(error);
                }
            }
        }

        [SecurityPermissionAttribute(SecurityAction.Demand, ControlThread = true)]
        private void KillTheThread()
        {
            thread.Abort();
        }
        // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MY CODE ENDS HERE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MY CODE ENDS HERE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MY CODE ENDS HERE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



        private void Start()
        {
            m_WheelMeshLocalRotations = new Quaternion[4];
            for (int i = 0; i < 4; i++)
            {
                m_WheelMeshLocalRotations[i] = m_WheelMeshes[i].transform.localRotation;
            }
            m_WheelColliders[0].attachedRigidbody.centerOfMass = m_CentreOfMassOffset;

            m_MaxHandbrakeTorque = float.MaxValue;

            m_Rigidbody = GetComponent<Rigidbody>();
            m_CurrentTorque = m_FullTorqueOverAllWheels - (m_TractionControl * m_FullTorqueOverAllWheels);

            InitilizeWork();
        }






        private void GearChanging()
        {
            float f = Mathf.Abs(CurrentSpeed / MaxSpeed);
            float upgearlimit = (1 / (float)NoOfGears) * (m_GearNum + 1);
            float downgearlimit = (1 / (float)NoOfGears) * m_GearNum;

            if (m_GearNum > 0 && f < downgearlimit)
            {
                m_GearNum--;
            }

            if (f > upgearlimit && (m_GearNum < (NoOfGears - 1)))
            {
                m_GearNum++;
            }
        }


        // simple function to add a curved bias towards 1 for a value in the 0-1 range
        private static float CurveFactor(float factor)
        {
            return 1 - (1 - factor) * (1 - factor);
        }


        // unclamped version of Lerp, to allow value to exceed the from-to range
        private static float ULerp(float from, float to, float value)
        {
            return (1.0f - value) * from + value * to;
        }


        private void CalculateGearFactor()
        {
            float f = (1 / (float)NoOfGears);
            // gear factor is a normalised representation of the current speed within the current gear's range of speeds.
            // We smooth towards the 'target' gear factor, so that revs don't instantly snap up or down when changing gear.
            var targetGearFactor = Mathf.InverseLerp(f * m_GearNum, f * (m_GearNum + 1), Mathf.Abs(CurrentSpeed / MaxSpeed));
            m_GearFactor = Mathf.Lerp(m_GearFactor, targetGearFactor, Time.deltaTime * 5f);
        }


        private void CalculateRevs()
        {
            // calculate engine revs (for display / sound)
            // (this is done in retrospect - revs are not used in force/power calculations)
            CalculateGearFactor();
            var gearNumFactor = m_GearNum / (float)NoOfGears;
            var revsRangeMin = ULerp(0f, m_RevRangeBoundary, CurveFactor(gearNumFactor));
            var revsRangeMax = ULerp(m_RevRangeBoundary, 1f, gearNumFactor);
            Revs = ULerp(revsRangeMin, revsRangeMax, m_GearFactor);
        }


        public void Move(float steering, float accel, float footbrake, float handbrake)
        {
            //Debug.Log(steering+" "+ accel+" "+footbrake+" "+handbrake);
            turn = steering;
            forward = accel;
            for (int i = 0; i < 4; i++)
            {
                Quaternion quat;
                Vector3 position;
                m_WheelColliders[i].GetWorldPose(out position, out quat);
                m_WheelMeshes[i].transform.position = position;
                m_WheelMeshes[i].transform.rotation = quat;
            }

            //clamp input values
            steering = Mathf.Clamp(steering, -1, 1);
            AccelInput = accel = Mathf.Clamp(accel, 0, 1);
            BrakeInput = footbrake = -1 * Mathf.Clamp(footbrake, -1, 0);
            handbrake = Mathf.Clamp(handbrake, 0, 1);

            //Set the steer on the front wheels.
            //Assuming that wheels 0 and 1 are the front wheels.
            m_SteerAngle = steering * (m_MaximumSteerAngle)/*4*/;
            m_WheelColliders[0].steerAngle = m_SteerAngle;
            m_WheelColliders[1].steerAngle = m_SteerAngle;

            SteerHelper();
            ApplyDrive(accel, footbrake);
            CapSpeed();

            //Set the handbrake.
            //Assuming that wheels 2 and 3 are the rear wheels.
            if (handbrake > 0f)
            {
                var hbTorque = handbrake * m_MaxHandbrakeTorque;
                m_WheelColliders[2].brakeTorque = hbTorque;
                m_WheelColliders[3].brakeTorque = hbTorque;
            }


            CalculateRevs();
            GearChanging();

            AddDownForce();
            CheckForWheelSpin();
            TractionControl();
        }


        private void CapSpeed()
        {
            float speed = m_Rigidbody.velocity.magnitude;
            switch (m_SpeedType)
            {
                case SpeedType.MPH:

                    speed *= 2.23693629f;
                    if (speed > m_Topspeed)
                        m_Rigidbody.velocity = (m_Topspeed / 2.23693629f) * m_Rigidbody.velocity.normalized;
                    break;

                case SpeedType.KPH:
                    speed *= 3.6f;
                    if (speed > m_Topspeed)
                        m_Rigidbody.velocity = (m_Topspeed / 3.6f) * m_Rigidbody.velocity.normalized;
                    break;
            }
        }


        private void ApplyDrive(float accel, float footbrake)
        {

            float thrustTorque;
            switch (m_CarDriveType)
            {
                case CarDriveType.FourWheelDrive:
                    thrustTorque = accel * (m_CurrentTorque / 4f);

                    for (int i = 0; i < 4; i++)
                    {
                        m_WheelColliders[i].motorTorque = thrustTorque;
                    }
                    break;

                case CarDriveType.FrontWheelDrive:
                    thrustTorque = accel * (m_CurrentTorque / 2f);
                    m_WheelColliders[0].motorTorque = m_WheelColliders[1].motorTorque = thrustTorque;
                    break;

                case CarDriveType.RearWheelDrive:
                    thrustTorque = accel * (m_CurrentTorque);
                    m_WheelColliders[2].motorTorque = m_WheelColliders[3].motorTorque = thrustTorque;
                    break;

            }

            for (int i = 0; i < 4; i++)
            {
                if (CurrentSpeed > 5 && Vector3.Angle(transform.forward, m_Rigidbody.velocity) < 50f)
                {
                    m_WheelColliders[i].brakeTorque = m_BrakeTorque * footbrake;
                }
                else if (footbrake > 0)
                {
                    m_WheelColliders[i].brakeTorque = 0f;
                    m_WheelColliders[i].motorTorque = -m_ReverseTorque * footbrake;
                }
            }
        }


        private void SteerHelper()
        {
            for (int i = 0; i < 4; i++)
            {
                WheelHit wheelhit;
                m_WheelColliders[i].GetGroundHit(out wheelhit);
                if (wheelhit.normal == Vector3.zero)
                    return; // wheels arent on the ground so dont realign the rigidbody velocity
            }

            // this if is needed to avoid gimbal lock problems that will make the car suddenly shift direction
            if (Mathf.Abs(m_OldRotation - transform.eulerAngles.y) < 10f)
            {
                var turnadjust = (transform.eulerAngles.y - m_OldRotation) * m_SteerHelper;
                Quaternion velRotation = Quaternion.AngleAxis(turnadjust, Vector3.up);
                m_Rigidbody.velocity = velRotation * m_Rigidbody.velocity;
            }
            m_OldRotation = transform.eulerAngles.y;
        }


        // this is used to add more grip in relation to speed
        private void AddDownForce()
        {
            m_WheelColliders[0].attachedRigidbody.AddForce(-transform.up * m_Downforce *
                                                         m_WheelColliders[0].attachedRigidbody.velocity.magnitude);
        }


        // checks if the wheels are spinning and is so does three things
        // 1) emits particles
        // 2) plays tiure skidding sounds
        // 3) leaves skidmarks on the ground
        // these effects are controlled through the WheelEffects class
        private void CheckForWheelSpin()
        {
            // loop through all wheels
            for (int i = 0; i < 4; i++)
            {
                WheelHit wheelHit;
                m_WheelColliders[i].GetGroundHit(out wheelHit);

                // is the tire slipping above the given threshhold
                if (Mathf.Abs(wheelHit.forwardSlip) >= m_SlipLimit || Mathf.Abs(wheelHit.sidewaysSlip) >= m_SlipLimit)
                {
                    m_WheelEffects[i].EmitTyreSmoke();

                    // avoiding all four tires screeching at the same time
                    // if they do it can lead to some strange audio artefacts
                    if (!AnySkidSoundPlaying())
                    {
                        m_WheelEffects[i].PlayAudio();
                    }
                    continue;
                }

                // if it wasnt slipping stop all the audio
                if (m_WheelEffects[i].PlayingAudio)
                {
                    m_WheelEffects[i].StopAudio();
                }
                // end the trail generation
                m_WheelEffects[i].EndSkidTrail();
            }
        }

        // crude traction control that reduces the power to wheel if the car is wheel spinning too much
        private void TractionControl()
        {
            WheelHit wheelHit;
            switch (m_CarDriveType)
            {
                case CarDriveType.FourWheelDrive:
                    // loop through all wheels
                    for (int i = 0; i < 4; i++)
                    {
                        m_WheelColliders[i].GetGroundHit(out wheelHit);

                        AdjustTorque(wheelHit.forwardSlip);
                    }
                    break;

                case CarDriveType.RearWheelDrive:
                    m_WheelColliders[2].GetGroundHit(out wheelHit);
                    AdjustTorque(wheelHit.forwardSlip);

                    m_WheelColliders[3].GetGroundHit(out wheelHit);
                    AdjustTorque(wheelHit.forwardSlip);
                    break;

                case CarDriveType.FrontWheelDrive:
                    m_WheelColliders[0].GetGroundHit(out wheelHit);
                    AdjustTorque(wheelHit.forwardSlip);

                    m_WheelColliders[1].GetGroundHit(out wheelHit);
                    AdjustTorque(wheelHit.forwardSlip);
                    break;
            }
        }


        private void AdjustTorque(float forwardSlip)
        {
            if (forwardSlip >= m_SlipLimit && m_CurrentTorque >= 0)
            {
                m_CurrentTorque -= 10 * m_TractionControl;
            }
            else
            {
                m_CurrentTorque += 10 * m_TractionControl;
                if (m_CurrentTorque > m_FullTorqueOverAllWheels)
                {
                    m_CurrentTorque = m_FullTorqueOverAllWheels;
                }
            }
        }


        private bool AnySkidSoundPlaying()
        {
            for (int i = 0; i < 4; i++)
            {
                if (m_WheelEffects[i].PlayingAudio)
                {
                    return true;
                }
            }
            return false;
        }
    }
}