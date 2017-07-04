			function myFunction() {
				var times = document.getElementById("select").value;
				var s = "";
				for(var i = 2; i <= times; ++i) {
					s += "User ";
					s += i;
					s += " <input id = 'user_";
					s += i;
					s += "'";
					s += " name = 'user_";
					s += i;
					s += "'";
					s += " type = 'text' value = '' />";
					s += "<br><br>";
				}
				document.getElementById("demo").innerHTML = s;
			}
