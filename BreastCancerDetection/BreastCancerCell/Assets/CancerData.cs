
public class CancerData {
    public float thickness = 0;
    public float size = 0;
    public float shape = 0;
    public float adhesion = 0;
    public float epi = 0;
    public float bare = 0;
    public float bland = 0;
    public float normal = 0;
    public float mitoses = 0;
    public float trainedOn = 0;
    public float predictionOutput1 = 0;
    public float predictionOutput2 = 0;
    public float actualOutput1 = 0;
    public float actualOutput2 = 0;

    public CancerData(float thickness, float size, float shape, float adhesion, float epi, float bare, float bland, float normal, float mitoses)
    {
        this.thickness = thickness;
        this.size = size;
        this.shape = shape;
        this.adhesion = adhesion;
        this.epi = epi;
        this.bare = bare;
        this.bland = bland;
        this.normal = normal;
        this.mitoses = mitoses;
    }

    public CancerData(float trainedOn, float thickness, float size, float shape, float adhesion, float epi, float bare, float bland, float normal, float mitoses, float actualOutput1, float actualOutput2, float predictionOutput1, float predictionOutput2)
    {
        this.thickness = thickness;
        this.size = size;
        this.shape = shape;
        this.adhesion = adhesion;
        this.epi = epi;
        this.bare = bare;
        this.bland = bland;
        this.normal = normal;
        this.mitoses = mitoses;
        this.predictionOutput1 = predictionOutput1;
        this.predictionOutput2 = predictionOutput2;
        this.actualOutput1 = actualOutput1;
        this.actualOutput2 = actualOutput2;
        this.trainedOn = trainedOn;
    }

    public CancerData(CancerData data)
    {
        this.thickness = data.thickness;
        this.size = data.size;
        this.shape = data.shape;
        this.adhesion = data.adhesion;
        this.epi = data.epi;
        this.bare = data.bare;
        this.bland = data.bland;
        this.normal = data.normal;
        this.mitoses = data.mitoses;
        this.predictionOutput1 = data.predictionOutput1;
        this.predictionOutput2 = data.predictionOutput2;
        this.actualOutput1 = data.actualOutput1;
        this.actualOutput2 = data.actualOutput2;
        this.trainedOn = data.trainedOn;
    }
}
