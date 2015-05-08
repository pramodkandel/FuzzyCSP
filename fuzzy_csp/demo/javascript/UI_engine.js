var round=0;
var preferences = [];
var u;

function stringifyPreferences (preferences,i,j)
{
	var str; 
	if (j == "0") {
		str = preferences[i].combined.main + ", " + preferences[i].combined.side + " and " + preferences[i].combined.drink;	
	} else if (j == "1") {
		str = preferences[i].desirability.main + ", " + preferences[i].desirability.side + " and " + preferences[i].desirability.drink;	
	} else if (j == "2") {
		str = preferences[i].availability.main + ", " + preferences[i].availability.side + " and " + preferences[i].availability.drink;	
	}
	return str;
}

function getNextPreference(attempt) {
	document.getElementById("robot").src="images/waiting.gif";
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/sendNextPreference",
		data: { attempt: attempt},
		dataType: 'text'
	}).done(function ( response ) {
			//alert(response);
			preferences.push(JSON.parse(response));
			
			if (attempt == 1) {
				document.getElementById("alternate_choice_explain").style.visibility='visible';
				
				document.getElementById("alternate_choice_explain").innerHTML= "<br>" + " Hmmm.. let me see. Your most favourite breakfast " + stringifyPreferences(preferences,0,1) + " was low on stock, the best I could do was " + stringifyPreferences(preferences,0,0) + ". But since you didnt like it, how about " + stringifyPreferences(preferences,1,0) + "?" + "<br>What would you like to go along?";
				
				 document.getElementById("alt_choice_1_yes").style.visibility='visible';
				 document.getElementById("alt_choice_1_no").style.visibility='visible';

				 u.text = " Okay. Let me see. Your most favourite breakfast " + stringifyPreferences(preferences,0,1) + " was low on stock, the best I could do was " + stringifyPreferences(preferences,0,0) + ". But since you did not like it, how about " + stringifyPreferences(preferences,1,0) + "?";
				 speechSynthesis.speak(u);	
				 u.text= "Would you like to go along?";
				 speechSynthesis.speak(u);

			} else if (attempt == 2) {
				document.getElementById("alt_choice_2_explain").style.visibility='visible';
				document.getElementById("alt_choice_2").innerHTML=stringifyPreferences(preferences,2,0) + "?";
				document.getElementById("alt_choice_2_yes").style.visibility='visible';
				document.getElementById("alt_choice_2_no").style.visibility='visible';
				
				u.text = " You are testing my precarious algorithms at this point and also my shaky processing power! Ha, I am just being modest.";
				speechSynthesis.speak(u);		
				u.text= "How about?" + stringifyPreferences(preferences,2,0) + "?";
				speechSynthesis.speak(u);

			} else if (attempt == 3) {
				document.getElementById("alt_choice_3_explain").style.visibility='visible';
				document.getElementById("alt_choice_3").innerHTML=stringifyPreferences(preferences,3,0) + "!";
				u.text="This is the last choice I can give you at this point!";
				speechSynthesis.speak(u);	
				u.text=stringifyPreferences(preferences,3,0);
				speechSynthesis.speak(u);				
			}
	});
}

function finalizeMainPreference () {
	alert ("You are all set");
}

function addPreference (options) {
	preferences.push(JSON.parse(options));
}

function init () {
	u = new SpeechSynthesisUtterance();
	u.text = "Hello Human";
	speechSynthesis.speak(u);
	document.getElementById("robot").src="images/forbidden-fruit.gif";
	// Get the best preferences based on desirability, availability and combined
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/"
	}).done(function ( response ) {
			
			preferences.push(JSON.parse(response));
			//console.log(JSON.stringify(preferences));
			document.getElementById("preference_initial").innerHTML = preferences[0].combined.main + ", " + preferences[0].combined.side + " and " + preferences[0].combined.drink;
			u.text="Good Morning! How would you like "+ stringifyPreferences(preferences,0,0) + " to have for breakfast today?";
			speechSynthesis.speak(u);
	});	
	
}

window.onload =init;