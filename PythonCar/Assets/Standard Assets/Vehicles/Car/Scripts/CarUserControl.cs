using System;
using UnityEngine;
using UnityStandardAssets.CrossPlatformInput;

namespace UnityStandardAssets.Vehicles.Car
{
    [RequireComponent(typeof (CarController))]
    public class CarUserControl : MonoBehaviour
    {
        private CarController m_Car; // the car controller we want to use


        private void Awake()
        {
            // get the car controller
            m_Car = GetComponent<CarController>();
        }


        private void FixedUpdate()
        {
            // pass the input to the car!
            float h = CrossPlatformInputManager.GetAxis("Horizontal");
            if (h < 0)
                h = -1f;
            else if (h > 0)
                h = 1f;
            float v = CrossPlatformInputManager.GetAxis("Vertical");

            if (v < 0)
                v = -1f;
            else if (v > 0)
                v = 1f;

            float handbrake = CrossPlatformInputManager.GetAxis("Jump");

            m_Car.Move(h, v, v, handbrake);
        }
    }
}
