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

		echo($output[0]);
?>