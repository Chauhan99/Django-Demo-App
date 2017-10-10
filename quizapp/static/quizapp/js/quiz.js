function startquiz()
{
	alert("The quiz is about to start. Click 'ok' when u are ready !");
	token=document.getElementsByName('csrfmiddlewaretoken')[0].value;  
 	$.post('/quizapp/loadquiz/',{'csrfmiddlewaretoken':token},function(mquestion)
		{
			$('#quiz-content').html(mquestion);
		});
};

function loadquiz()
{
	token=document.getElementsByName('csrfmiddlewaretoken')[0].value;  
 	$.post('/quizapp/loadquiz/',{'csrfmiddlewaretoken':token},function(mquestion)
		{
			$('#quiz-content').html(mquestion);
		});
}

function submitanswer()
{
	token=document.getElementsByName('csrfmiddlewaretoken')[0].value;  
	selected=$("input[name=selected]:checked").val()
	$.post('/quizapp/loadquiz/',{'csrfmiddlewaretoken':token,'selected':selected},function(mquestion)
		{
			$('#quiz-content').html(mquestion);
		});
}

function fetch_leaderboard()
{
	//alert("Fetching leaderboard");
	token=document.getElementsByName('csrfmiddlewaretoken')[0].value;  
 	$.post('/quizapp/leaderboard/',{'csrfmiddlewaretoken':token},function(mleaderboard)
 		{
 			$('#leaderboard-content').html(mleaderboard);
 		});   
};

function fetch_profiledata()
{
	//alert("Fetching leaderboard");
	token=document.getElementsByName('csrfmiddlewaretoken')[0].value;  
 	$.post('/quizapp/loadprofile/',{'csrfmiddlewaretoken':token},function(mprofiledata)
 		{
 			$('#profile-content').html(mprofiledata);
 		});   
};

function fetch()
{
	fetch_profiledata();
	fetch_leaderboard();
};

