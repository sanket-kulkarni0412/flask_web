window.onload = () => {
	$('#sendbutton').click(() => {
		imagebox = $('#imagebox')
		class_name=$('#class1')
		score_ach=$('#score1')
		box_ach=$('#box1')
		input = $('#imageinput')[0]
		if(input.files && input.files[0])
		{
			let formData = new FormData();
			formData.append('image' , input.files[0]);
			$.ajax({
				url: "http://localhost:5001/detectObject", // fix this to your liking
				type:"POST",
				data: formData,
				cache: false,
				processData:false,
				contentType:false,
				error: function(data){
					console.log("upload error" , data);
					console.log(data.getAllResponseHeaders());
				},
				success: function(data){
					console.log(data);
					class1=data['class']
					score1=data['score']
					box1=data['boxes']
					bytestring = data['status']
					//image = bytestring.split('\'')[1]
					imagebox.attr('src' , 'data:image/jpeg;base64,'+bytestring)
					document.getElementById("class1").innerHTML = "Class Name = "+class1;
					document.getElementById("score1").innerHTML = "Score = "+score1;
					document.getElementById("box1").innerHTML = "B_box = "+box1;

					
				}
			});
		}
	});
};



function readUrl(input){
	imagebox = $('#imagebox')
	console.log("evoked readUrl")
	if(input.files && input.files[0]){
		let reader = new FileReader();
		reader.onload = function(e){
			// console.log(e)
			
			imagebox.attr('src',e.target.result); 
			imagebox.height(500);
			imagebox.width(800);
		}
		reader.readAsDataURL(input.files[0]);
	}

	
}