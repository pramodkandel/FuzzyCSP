
var want_items = [];
var no_want_items = [];
var desire_attempt = 0;
var available_attempt = 0;
var combined_attempt = 1; //the very initial recommendation is the combined solution

var rejected_sols = []
var cur_sol;

var rejected_num = 0;
var u;


$(document).ready(function(){
	init();

	$("#yes_btn").click(function(){
		text = "Enjoy your breakfast!";
		$("#human_response").html("");
		give_robot_response(text);
	})

	$("#no_btn").click(function(){
		//alert("No btn clicked.")
		//$("#robot_response_text").hide()
		rejected_sols.push(cur_sol)
		show_rejected_sols(rejected_sols)
		$("#yes_no_div").hide();
		request_new_input();
	})


	$( "#after_reject_form" ).submit(function( event ) {
		event.preventDefault();
		rejected_num += 1;
    	// get all the inputs into an array.
    	inputs = $("#after_reject_form").serializeArray();
    	var values = {};
    	for (var i=0; i<inputs.length; i++) {
    		input = inputs[i]
        	values[input.name] = input.value;
    	}

    	type = values.bf_type;
    	want_item = values.want.trim();
    	no_want_item = values.no_want.trim();
    	attempt_num = update_and_get_attempt_num(type, false)
    	if (want_item.length > 0) {
    		if (want_items.indexOf(want_item) == -1){
    			want_items.push(want_item);
    		}

    		//now check if user had said before they didn't want it
    		no_want_index = no_want_items.indexOf(want_item)
    		if (no_want_index > -1){
    			no_want_items.splice(no_want_index,1)
    		}
    		
    	}
    	if (no_want_item.length>0){
    		if (no_want_items.indexOf(no_want_item) == -1){
    			no_want_items.push(no_want_item);
    		}

    		//now check if user had said before they wanted it. If so,
    		//remove from want
    		want_index = want_items.indexOf(no_want_item)
    		if (want_index > -1){
    			want_items.splice(want_index,1)
    		}
    	}
    	
    	data = {"want":want_items.join(), "no_want":no_want_items.join(), "sol_type":type, "attempt":attempt_num, "rejected_sols":rejected_sols.join()}
		
    	//clear the form now
		getNextPreference(data);

	});

});


function show_rejected_sols(rejected_sols)
{
	show_text = ""
	if (rejected_sols.length >0){
		show_text = "Rejected:<br>"
	}
	for (var i=0; i<rejected_sols.length; i++){
		soln = rejected_sols[i];
		show_text += JSON.stringify(soln) + "<br>"
	}
	$("#rejected_info").html(show_text);
}

function update_and_get_attempt_num(type, do_reset)
{
	if (type == "availability"){
		available_attempt += 1;
		return available_attempt
	}
	else if (type == "desirability"){
		desire_attempt += 1;
		return desire_attempt
	}
	else if (type == "combined"){
		combined_attempt += 1;
		return combined_attempt
	}
	else {
		console.log("Wrong type provided in update_and_get_attempt_num function.")
	}

}


function getNextPreference(send_data) {
	$("#after_reject_form").hide();
	do_request_again = false;
	document.getElementById("robot").src="images/waiting.gif";
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/sendNextPreference",
		data: send_data,
		dataType: 'text'
	}).done(function ( response ) {
		//alert(response);
		json_response = JSON.parse(response);
		if (json_response.sol == null){
			str_response = "There is no breakfast combo available with "+
			"those choices. Please start from the beginning";
			give_robot_response(str_response);
			//renew all variables
			reset_all_variables();
			$("#rejected_info").html("");
			$("#yes_no_div").hide();
			request_new_input();
			return;
		}	
		str_response = get_string_response(json_response, false)
		give_robot_response(str_response);
		

		//if stock of any item is 0, request new inputs
		stock = json_response.stock;
		for (var i=0; i<stock.length; i++){
			if (stock[i] ==0) { 
				do_request_again = true;
				break;
			}
		}

		if (do_request_again){request_new_input();}
		else {$("#yes_no_div").show();}
		
	});
}

function request_new_input(){
	$( "#after_reject_form" ).show();
	$( "#after_reject_form" )[0].reset();
}

function reset_all_variables(){
	want_items = [];
	no_want_items = [];
	desire_attempt = 0;
	available_attempt = 0;
	combined_attempt = 1; //the very initial recommendation is the combined solution

	rejected_sols = []
	cur_sol = null;
	rejected_num = 0;
}

//Displays the text and speaks the text as a robot response
function give_robot_response(text){
	$("#robot_response_text").html(text);

	u = new SpeechSynthesisUtterance();
	u.text = text;
	speechSynthesis.speak(u);
}

function stringify_sol(solution){
	if (solution.length==1){return solution;}
	str = "";
	for (var i=0; i<solution.length; i++){
		if (i == solution.length-1){ str += " and "+solution[i];}
		else {str += solution[i] + ", "}
	}
	return str;
}

function get_string_response(json_response, is_init){
	sol = json_response.sol;
	cur_sol = sol;

	stock = json_response.stock;

	sol_string = stringify_sol(sol);
	sol_response = "";
	if (is_init) {sol_response = "I recommend "+sol_string+ " for today's breakfast.";}
	else {sol_response = "According to your choice, next best option is "+sol_string + ".";}
	
	stock_string = "";


	ran_out = false;
	for (var i=0; i<stock.length; i++){
		if (stock[i] == 0){
			stock_string = "However, "+sol[i] + " is out of stock. Please choose another option.";
			//take the item out of "want_items" if it's there
			if (want_items.indexOf(sol[i]) > -1){
				want_items.splice(want_items.indexOf(sol[i]),1)
			}
			ran_out = true;
		}
	}

	
	if (! ran_out){
		low_things = []
		for (var i=0; i<stock.length; i++){
			if (stock[i] == 1){
				low_things.push(sol[i]);
			}
		}
		if (low_things.length > 0){
			low_things_str = stringify_sol(low_things);
			is_or_are = "";
			if (low_things.length == 1){
				is_or_are = "is";
			}else{ is_or_are = "are";}
			stock_string = "However, "+low_things_str + is_or_are + " low on stock. Do you still want it?"
		}else{
			stock_string = "Would you want it?"
		}
	}

	return sol_response + " "+ stock_string
}

function init () {
	$("#after_reject_form").hide();
	give_robot_response("Good Morning.")
	document.getElementById("robot").src="images/forbidden-fruit.gif";
	// Get the best preferences based on desirability, availability and combined
	$.ajax({
		
		type: "GET",
		url: "http://localhost:5000/"
	}).done(function ( response ) {
			json_response = JSON.parse(response);
			
			str_response = get_string_response(json_response, true)

			give_robot_response(str_response);
	});	
	
}

