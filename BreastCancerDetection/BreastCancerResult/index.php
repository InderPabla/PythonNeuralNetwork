<?php 
	    // various cell infromation  
		// 0 represents unkown 		
		$thickness = $_GET["thickness"]; 
		$size = $_GET["size"]; 
		$shape = $_GET["shape"]; 
		$adhesion = $_GET["adhesion"]; 
		$epi = $_GET["epi"]; 
		$bare = $_GET["bare"]; 
		$bland = $_GET["bland"];  
		$normal = $_GET["normal"]; 
		$mitoses = $_GET["mitoses"];
		
		$python = 'C:\Users\Pabla\Anaconda3\envs\py34\python.exe'; //python.exe path
		$file = 'C:\Users\Pabla\Desktop\ImageAnalysis\PyAI\BreastCancerTester.py'; //python.exe path
		$cmd = "$python $file $thickness $size $shape $adhesion $epi $bare $bland $normal $mitoses"; //command line instruction to execute 
		exec("$cmd", $output); //execute and put python prints into output
		$out_result ="";
		
		if($output[0] == 0)
		{
			$out_result = "benign";
		}
		else
		{
			$out_result = "malignant";
		}
		
		echo ($out_result); 
		
		//C:\Users\Pabla\Anaconda3\envs\py34\python.exe C:\Users\Pabla\Desktop\ImageAnalysis\PyAI\BreastCancerTester.py
		//http://localhost:8000/BreastCancerResult/index.php?thickness=1&size=0&shape=0&adhesion=0&epi=0&bare=0&bland=0&normal=0&mitoses=0
		//http://localhost:8000/BreastCancerResult/index.php?thickness=1&size=1&shape=8&adhesion=1&epi=6&bare=1&bland=1&normal=3&mitoses=2
		//http://192.168.0.17:8000/BreastCancerResult/index.php?thickness=1&size=0&shape=0&adhesion=0&epi=0&bare=0&bland=0&normal=0&mitoses=0
?>