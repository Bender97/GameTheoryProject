<!DOCTYPE HTML>
<HTML>
<HEAD>

	<style>
		.container {
			background-color: white; margin:0 auto; display: flex;
			justify-content: center;
			align-items: center;
		}

		.sliderContainer {
			width: 20%; height: 200px; border: 1px solid black;
			padding: 10px;
		}

		.tableContainer {
			width: 40%; height: 400px;
		}

		.content {
			background-color: white; display: inline-block; margin:0 auto;
		}

		.title {
			width: 200px; height: 100px; background-color: white; margin:0 auto; border: 1px solid black;
		}

		table, td, th{
			border: 1px solid black;
			border-collapse: collapse;
			font-size:1.5vw;
			padding: 5px;
		}

		.slider {
			width: 100%;

		}

		td {
			text-align: center;
		}

		td.label {
			font-weight: bold;
		}
	</style>

	<script>

		var cell 		= Array.from(Array(4), _ => Array(4));
		var normalform 	= Array.from(Array(4), _ => Array.from(Array.from(Array(4), _ => Array(2))));

		var pF_R1 = 0.5;
		var pS_R1 = 1 - pF_R1;
		var pF_R2 = 0.5;
		var pS_R2 = 1 - pF_R2;

		var k1 = 200;
		var k2 = 0;
		var k3 = 0.1*k1;

		var idxs = ["NN", "NB", "BN", "BB"];

		function initVars() {

			initNEsTable();
			var i, j;
			for (i=0; i<4; i++) {
				for (j=0; j<4; j++) {
					cell[i][j] = document.getElementById(idxs[i]+idxs[j]);
				}
			}
		}

		function initNEsTable() {
			var i, j;
			var s = "";
			s += "<table>";

			s+="<tr><td></td>";
			for (i=0; i<idxs.length; i++)
				s += "<td class=\"label\">" + idxs[i] + "</td>";
			s+="</tr>";

			for (i=0; i<idxs.length; i++) {
				s+="<tr><td class=\"label\">" + idxs[i] + "</td>" ;
				for (j=0; j<normalform[0].length; j++)
					s += "<td id=\"" + idxs[i] + idxs[j] + "\"></td>";
				s+="</tr>";
			}
			s += "</table>";
			document.getElementById("NEs").innerHTML = s;
		}

		function printCells() {
			var i, j;

			for (i=0; i<4; i++) {
				for (j=0; j<4; j++) {
					word = idxs[i]+idxs[j];
					cell[i][j].innerHTML = normalform[i][j][0].toString() + ", " + normalform[i][j][1].toString();
				}
			}
		}

		function highlightNE() {
			var i, j;
			var br = Array.from(Array(4), _ => Array(4).fill(0));	// best responses

			// find best responses of player 1
				// find max per columns
			for (i=0; i<4; i++) {
				var max = -1000000;
				for (j=0; j<4; j++) {
					if (normalform[j][i][0]>max)
						max = normalform[j][i][0];
				}

				console.log("col " + i + " max: " + max);

				// all rows which have max as value, are eligible
				for (j=0; j<4; j++) {
					if (normalform[j][i][0]==max)
						br[j][i] = 1;
				}
			}

			// find best responses of player 1
				// find max per rows
			for (i=0; i<4; i++) {
				var max = -1000000;
				for (j=0; j<4; j++) {
					if (normalform[i][j][1]>max)
						max = normalform[i][j][1];
				}

				console.log("row " + i + " max: " + max);

				// all columns which have max as value, are eligible

				for (j=0; j<4; j++) {
					if (normalform[i][j][1]==max)
						br[i][j] += 1;
				}
			}


			for (i=0; i<4; i++) {
				for (j=0; j<4; j++) {
					if (br[i][j]==2) {
						cell[i][j].style.backgroundColor = "red";
					}
				}
			}
		}

		function resetStyles() {
			var i, j;
			for (i=0; i<4; i++)
				for (j=0; j<4; j++)
					cell[i][j].style.backgroundColor = "white";
		}

		function update() {

			resetStyles();

			var dmax = document.getElementById("dmax").value;
			var davg = document.getElementById("davg").value;
			var tmin = document.getElementById("tmin").value;
			var tavg = document.getElementById("tavg").value;


			var dict = {
				"SSNN": [davg - tmin - k2, davg-tmin-k2],
				"SSNB": [davg - tmin - k3, dmax-tavg-k3],
				"SSBN": [dmax - tavg - k3, davg-tmin-k3],
				"SSBB": [-tavg - k1, - tavg - k1],
				"SFNN": [davg-tmin-2*k2, tavg-tmin],
				"SFNB": [dmax-tavg-2*k3, davg-tmin],
				"SFBN": [davg-tmin-2*k3, dmax-tavg],
				"SFBB": [-tavg, dmax-tavg],
				"FSNN": [tavg-tmin, davg-tmin-2*k2],
				"FSNB": [davg-tmin, dmax-tavg-2*k3],
				"FSBN": [dmax-tavg, davg-tmin-2*k3],
				"FSBB": [dmax-tavg, -tavg],
				"FFNN": [davg - tmin - k2, davg-tmin-k2],
				"FFNB": [davg - tmin - k3, dmax-tavg-k3],
				"FFBN": [dmax - tavg - k3, davg-tmin-k3],
				"FFBB": [-tavg - k1, - tavg - k1]
			};

			
			var i, j;

			for (i=0; i<4; i++) {
				for (j=0; j<4; j++) {
					word = idxs[i]+idxs[j];
					normalform[i][j][0] = pS_R1*pS_R2*dict["SS"+word[0]+word[2]][0] + pS_R1*pF_R2*dict["SF"+word[0]+word[3]][0] + pF_R1*pS_R2*dict["FS"+word[1]+word[2]][0] + pF_R1*pF_R2*dict["FF"+word[1]+word[3]][0];
					normalform[i][j][1] = pS_R1*pS_R2*dict["SS"+word[0]+word[2]][1] + pS_R1*pF_R2*dict["SF"+word[0]+word[3]][1] + pF_R1*pS_R2*dict["FS"+word[1]+word[2]][1] + pF_R1*pF_R2*dict["FF"+word[1]+word[3]][1];
				}
			}

			printCells();
			highlightNE();

			findStrictDominancies();
		}

		function findStrictDominancies() {

			var tick = 0;
			var changed = true;

			// P1dom[i] = 0/1 -> row i is not/is strictly dominated;
			var P1dom = Array(normalform.length).fill(0);
			// P2dom[i] = 0/1 -> col i is not/is strictly dominated;
			var P2dom = Array(normalform[0].length).fill(0);

			do {
				var data;

				data = findStrictDominanciesP(P1dom, P2dom, tick);
				
				changed = data[0];
				P1dom 	= data[1];
				P2dom 	= data[2];

				tick+=1;
			} while (changed);

			printSimplifiedTable(normalform, P1dom, P2dom);
		}

		function findStrictDominanciesP(P1dom, P2dom, tick) {
			var i, j;
			var changed = false;

			var player1 = tick%2==0;
			var player2 = !player1;

			var playerDomination	= player1 ? P1dom : P2dom;
			var otherPDomination	= player2 ? P1dom : P2dom;
			var iterate_over		= player1 ? normalform.length : normalform[0].length;
			var parseOver			= player1 ? normalform[0].length : normalform.length;

			for (i=0; i<iterate_over; i++) {	// check if col i dominates any other col
				for (j=0; j<iterate_over; j++) {
					if (i!=j) {
						var flag = 0;	// col i must dominate col j in every row k which is not already dominated

						for (k=0; k<parseOver; k++) {
							if(otherPDomination[k]!=1 && ((player1 && normalform[i][k][0]<=normalform[j][k][0]) || (player2 && normalform[k][i][1]<=normalform[k][j][1]))) {
								flag = 1;
								break;
							}
						}
						if (flag==0) {// col i dominates col j
							if (playerDomination[j]==0)
								changed = true;
							playerDomination[j] = 1;
						}
					}
				}
			}

			if (player1)
				return [changed, playerDomination, P2dom];
			return [changed, P1dom, playerDomination]; 	// if player2
		}

		function printSimplifiedTable(normalform, P1dom, P2dom) {
			var i, j;
			var s = "<table><tr><td></td>";

			for (j=0; j<normalform[0].length; j++)
				if (P2dom[j]==0)
					s+="<td class=\"label\">" + idxs[j] + "</td>";
			s+="</tr>";

			for (i=0; i<normalform.length; i++) 
				if (P1dom[i]==0) {
					s+="<tr><td class=\"label\">" + idxs[i] + "</td>" ;
					for (j=0; j<normalform[0].length; j++)
						if (P2dom[j]==0)
							s += "<td>" + normalform[i][j][0] + ", " + normalform[i][j][1] + "</td>";
					s+="</tr>";
				}
			
			s += "</table>";

			document.getElementById("simplifiedTable").innerHTML = s;
		}

		function updateValue(id) {
			elem = document.getElementById(id);
			document.getElementById(id+"_value").textContent = elem.value;
		}

	</script>
</HEAD>

<BODY>


	<div class="title" style="margin-top: 40px;"></div>
	

	<div class = "container sliderContainer" style="width: 20%; height: 200px; margin-left: 15%;  margin-top: 40px;">
		<div class="content" style = "width:100%;">
			<span>dmax </span><span id="dmax_value"></span>
			<input type="range" min="1" max="800" value="800" class="slider" id="dmax" onchange="updateValue('dmax'); update();">
			<span>davg </span><span id="davg_value"></span>
			<input type="range" min="1" max="800" value="200" class="slider" id="davg" onchange="updateValue('davg'); update();">
		</div>
	</div>

	<div class = "container sliderContainer" style="margin-right: 15%; margin-top: -200px;">
  		<div class="content" style = "width:100%;">
			<span>tmin </span><span id="tmin_value"></span>
			<input type="range" min="1" max="150" value="80" class="slider" id="tmin" onchange="updateValue('tmin'); update();">
			<span>tavg </span><span id="tavg_value"></span>
			<input type="range" min="1" max="150" value="150" class="slider" id="tavg" onchange="updateValue('tavg'); update();">
	  	</div>
	</div>

	<div style="border: 1px solid black; margin-top: 40px; background-color: white; padding:40px;" class ="container">

		<div class = "container tableContainer" style="border: 1px solid black;margin-left: 5%;">
			<div class = "content" id="NEs"></div>
		</div>

		<div class = "container" style=" border: 1px solid black; padding: 5px;">
			<div class = "content" id="button"><input type="button" value="update" onclick="update();"/></div>
		</div>

		<div class = "container tableContainer" style="border: 1px solid black;margin-right: 5%; ">
			<div class = "content" id="simplifiedTable"></div>
		</div>
	</div>

	

	<script>
		initVars();
		update();
		updateValue('dmax');
		updateValue('davg');
		updateValue('tmin');
		updateValue('tavg');
	</script>
</BODY>
</HTML>
