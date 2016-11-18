using UnityEngine;
using System.Collections;
using UnityEngine.UI;
using System;
using System.IO;
using System.Collections.Generic;

public class CancerDetector : MonoBehaviour {
    //5.72377854543 error

    public InputField predictionField;
    public InputField thicknessField;
    public InputField sizeField;
    public InputField shapeField;
    public InputField adhesionField;
    public InputField epiField;
    public InputField bareField;
    public InputField blandField;
    public InputField normalField;
    public InputField mitosesField;
    public Text predictionText;

    private string retrievePage = "http://localhost:8000/BreastCancerResult/index.php?";
    private bool done = false;
    private WWW web = null;

    public GameObject cancerTestPrefab;
    GameObject cancerTest;
    List<CancerData> cancerDataList = new List<CancerData>();
    int index = 0;
    // Use this for initialization
    void Start ()
    {
       

        /*System.Diagnostics.Process p = new System.Diagnostics.Process();
        p.StartInfo = new System.Diagnostics.ProcessStartInfo("explorer.exe");
        p.Start();*/
        

        thicknessField.text = "0";
        sizeField.text = "0";
        shapeField.text = "0";
        adhesionField.text = "0";
        epiField.text = "0";
        bareField.text = "0";
        blandField.text = "0";
        normalField.text = "0";
        mitosesField.text = "0";

    }
	
	// Update is called once per frame
	void Update ()
    {
	
	}

    public void OnNextButtonPress()
    {
        if (cancerDataList.Count > 0)
        {
            index++;
            if (index >= cancerDataList.Count)
            {
                index = 0;
            }

            Set();
        }
    }

    public void OnPreviousButtonPress()
    {
        if (cancerDataList.Count > 0)
        {
            index--;
            if (index <0)
            {
                index = cancerDataList.Count-1;
            }

            Set();
        }
    }

    public void OnCheckButtonPress()
    {
        if (!thicknessField.text.Equals("") && IsDigitsOnly(thicknessField.text) &&
            !sizeField.text.Equals("") && IsDigitsOnly(sizeField.text) &&
            !shapeField.text.Equals("") && IsDigitsOnly(shapeField.text) &&
            !adhesionField.text.Equals("") && IsDigitsOnly(adhesionField.text) &&
            !epiField.text.Equals("") && IsDigitsOnly(epiField.text) &&
            !bareField.text.Equals("") && IsDigitsOnly(bareField.text) &&
            !blandField.text.Equals("") && IsDigitsOnly(blandField.text) &&
            !normalField.text.Equals("") && IsDigitsOnly(normalField.text) &&
            !mitosesField.text.Equals("") && IsDigitsOnly(mitosesField.text))
        {
            StartCoroutine(GetResult());

            if (cancerTest != null)
            {
                Destroy(cancerTest);
            }

            cancerTest = Instantiate(cancerTestPrefab);
            for (int i = 0; i < cancerTest.transform.childCount; i++)
            {
                Transform cell = cancerTest.transform.GetChild(i);
                if (i == 0)
                {
                    cell.SendMessage("Activate",new CancerData(float.Parse(thicknessField.text), 
                                                               float.Parse(sizeField.text), 
                                                               float.Parse(shapeField.text),
                                                               float.Parse(adhesionField.text),
                                                               float.Parse(epiField.text),
                                                               float.Parse(bareField.text),
                                                               float.Parse(blandField.text),
                                                               float.Parse(normalField.text),
                                                               float.Parse(mitosesField.text)));
                }
                else
                {
                    cell.SendMessage("Activate", new CancerData(0,0,0,0,0,0,0,0,4));
                }
            }
        }
    }

    public void OnLoadButtonPress()
    {
        if (File.Exists(predictionField.text))
        {
            StreamReader reader = new StreamReader(predictionField.text);
            string line;
            cancerDataList = new List<CancerData>();
            index = 0;
            while (!reader.EndOfStream)
            {
                line = reader.ReadLine();
                string[] split = line.Split('\n', ' ');//System.Text.RegularExpressions.Regex.Split(line, @"\s{2,}");

                double[] output = Array.ConvertAll(split, new Converter<string, double>(Double.Parse));
                CancerData data = new CancerData((float)output[0], (float)output[1], (float)output[2], (float)output[3], (float)output[4], (float)output[5], (float)output[6], (float)output[7], (float)output[8], (float)output[9], (float)output[10], (float)output[11], (float)output[12], (float)output[13]);
                cancerDataList.Add(data);
            }

            reader.Close();
            Set();
        }
    }

    public void Set()
    {
        CancerData data = cancerDataList[index];

        thicknessField.text = data.thickness+"";
        sizeField.text = data.shape + "";
        shapeField.text = data.size + "";
        adhesionField.text = data.adhesion + "";
        epiField.text = data.epi + "";
        bareField.text = data.bare + "";
        blandField.text = data.bland + "";
        normalField.text = data.normal + "";
        mitosesField.text = data.mitoses + "";

        if (cancerTest != null)
        {
            Destroy(cancerTest);
        }

        cancerTest = Instantiate(cancerTestPrefab);
        for (int i = 0; i < cancerTest.transform.childCount; i++)
        {
            Transform cell = cancerTest.transform.GetChild(i);
            if (i == 0)
            {
                cell.SendMessage("Activate", data);
            }
            else
            {
                cell.SendMessage("Activate", new CancerData(0, 0, 0, 0, 0, 0, 0, 0, 4));
            }
        }


        if (data.predictionOutput1 > data.predictionOutput2)
        {
            float certainty = (float)((((1f - Math.Abs(1f - data.predictionOutput1)) + Math.Abs(1f - data.predictionOutput2)) / 2f) * 100f);
            float realCertainty = (float)((((1f - Math.Abs(1f - data.actualOutput1)) + Math.Abs(1f - data.actualOutput2)) / 2f) * 100f);
            predictionText.text = "Prediction: Benign :: Actual: "+ (data.actualOutput1> data.actualOutput2?"Benign :: ": "Malignant :: ") + "Certainty: " + (certainty.ToString("#0.00")) + "%\nError: " + Math.Abs(certainty-realCertainty).ToString("#0.00") + "% :: Data #: " + (index + 1) + "/" + cancerDataList.Count + " :: Used In Traning: " + (data.trainedOn == 1 ? "Yes" : "No");
            predictionText.color = Color.green;
        }
        else
        {
            float certainty = (float)((((1f - Math.Abs(1f - data.predictionOutput2)) + Math.Abs(1f - data.predictionOutput1)) / 2f) * 100f);
            float realCertainty = (float)((((1f - Math.Abs(1f - data.actualOutput2)) + Math.Abs(1f - data.actualOutput1)) / 2f) * 100f);
            predictionText.text = "Prediction: Malignant :: Actual: " + (data.actualOutput1 > data.actualOutput2 ? "Benign :: " : "Malignant :: ") + "Certainty: " + (certainty.ToString("#0.00")) + "%\nError: " + Math.Abs(certainty - realCertainty).ToString("#0.00") + "% :: Data #: " + (index + 1) + "/" + cancerDataList.Count + " :: Used In Traning: " + (data.trainedOn == 1 ? "Yes" : "No");
            predictionText.color = Color.red;
        }
    }

    public IEnumerator GetResult()
    {
        string page = retrievePage; //retrieve page
        predictionText.text = "N/A";
        predictionText.color = Color.white;

        page +=
            "thickness=" + thicknessField.text +
            "&size=" + sizeField.text +
            "&shape=" + shapeField.text +
            "&adhesion=" + adhesionField.text +
            "&epi=" + epiField.text +
            "&bare=" + bareField.text +
            "&bland=" + blandField.text +
            "&normal=" + normalField.text +
            "&mitoses=" + mitosesField.text;  

        done = false; //set to fasle to wait for web to return

        web = new WWW(page); //run page
        yield return web; //wait for web to execute url

        string[] split = System.Text.RegularExpressions.Regex.Split(web.text, @"\s{2,}");

        double[] output = Array.ConvertAll(split, new Converter<string, double>(Double.Parse));

        if (output[0] > output[1])
        {
            float certainty = (float)((((1f - Math.Abs(1f - output[0])) + Math.Abs(1f - output[1])) / 2f) * 100f);
            predictionText.text = "Benign Cancer :: Certainty:" + (certainty.ToString("#0.00")) + "%";
            predictionText.color = Color.green;
        }
        else
        {
            float certainty = (float)((((1f - Math.Abs(1f - output[1])) + Math.Abs(1f - output[0])) / 2f) * 100f);
            predictionText.text = "Malignant Cancer :: Certainty:" + (certainty.ToString("#0.00")) + "%";
            predictionText.color = Color.red;
        }

        done = true; //retrieved is true
    }

    bool IsDigitsOnly(string str)
    {
        foreach (char c in str)
        {
            if (c < '0' || c > '9')
                return false;
        }

        return true;
    }
}
