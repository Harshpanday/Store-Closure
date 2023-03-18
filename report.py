from weasyprint import HTML,CSS
from weasyprint.fonts import FontConfiguration
query="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pretium quis 
        mauris et pellentesque. In vitae accumsan metus. Vivamus iaculis dui ac elit egestas posuere. Vivamus porta maximus 
        metus, a maximus nunc egestas at. Aenean interdum fermentum arcu, eget iaculis lorem mollis eget. Sed et velit 
        malesuada, ultrices ante et, vehicula ipsum. Phasellus nisl urna, malesuada ac vehicula eget, mattis vel nisl. Duis 
        volutpat vulputate ornare."""

font_config = FontConfiguration()
html = HTML(string = f'''
    <html>
    <body>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <div><center><b><h2>ICICLE: Intelligent CyberInfrastructure with Computational Learning in the Environment</h2></b></center></div>
    <br>
    <br>
    <br>
    <img class="cover" src="ICICLE.jpeg">
    <br>
    <div><center><h2><b> <i> Food Policy Simulation Model Report </i> </b></h2></center></div>
    <p style="page-break-before: always" ></p>
    
    <head><b><center><h2>ICICLE- Food Policy Simulation Model Report</h2></center></b></head>
    
    <p><b>To:</b> Joe Mazzola, Health Commissioner, Franklin County Public Health</p>
    <p><b>From:</b> ICICLE Food Policy Simulation Use Case Team (Contact: Ayaz Hyder at <a href="hyder.22@osu.edu">hyder.22@osu.edu</a>)</p>
    <hr>
    <div>
        <b>Orignal Query -> </b> {query}
    </div>
    <br>
    <br>
    <div>
        <b>Interpreted Query -> </b> {query}
    </div>
    <br>
    <br>
    <table class="center">
        <tr>
            <th><b><center>Old</center></b></th>
            <th><b><center>New</center></b></th>
        </tr>
        <tr>
            <td><center><img src="./figures/map_before.png" style="width:300px;height:300px;"></center></td>
            <td><center><img src="./figures/map_after.png" style="width:300px;height:300px;"></center></td>
        </tr>
        <tr>
            <td colspan="2"><b>Figure:</b>{query}</td>
        </tr>
    </table>
    <p style="page-break-before: always" ></p>
    <table>
    <caption> <center> <h3><b> Overall Comparision </b></h3> </center> </caption>
    <tr>
        <td class="content"> <b>Description </b> {query}
        <br>
        <br>
         <b>Pattern</b> {query}
        <br> 
        <br>
        <b> Our Reccomendations: </b> {query}</td>
        <td class="image"><center><img src="./figures/overallcomparison.png" style="width:300px;height:300px;"></center></td>
    </tr>
    </table>
    <p style="page-break-before: always" ></p>
    <table>
    <caption> <center><h3> <b> Detailed Analysis </b> </h3></center> </caption>
    <tr>
        <td class="content"> <b>Description </b> {query}
        <br>
        <br>
         <b>Pattern</b> {query}
        <br> 
        <br>
        <b> Our Reccomendations: </b>{query}
    </td>
        <td class="image">
            <center><img src="./figures/ERHC.png" style="width:200px;height:200px;"></center>
            <center><img src="./figures/ERLC.png" style="width:200px;height:200px;"></center>
            <center><img src="./figures/LRHC.png" style="width:200px;height:200px;"></center>
            <center><img src="./figures/LRLC.png" style="width:200px;height:200px;"></center>
    </td>
    </tr>
    </table>
    <body>
</html>''',base_url='./')
css = CSS(string=
            '''
            @font-face{
                font-family: "Times New Roman", Times, serif;
            }
            body,html{
                font-family: "Times New Roman", Times, serif;
                height: 100%;
                margin: 0;
            }
            .bg {
                background-image: url("ICICLE.jpeg");
                height: 100%; 
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
                }
            img.cover{
                display:block;
                margin-left: auto; 
                margin-right: auto;
                width:70%; 
                height:24%;
                
                }
            .center{
                margin-left: auto;
                margin-right: auto;
            }
            div {
                text-align: justify;
                text-justify: inter-word;
                
            }
            div.container {
                display:inline-block;
            }
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                padding: 10;
            }
            td.content{
                width:300px;
            }
            td.image{
                width:350px;
            }
            #content {
                position: relative;
            }
            #content img {
                position: absolute;
                top: 0px;
                right: 0px;
            }
            ''',font_config=font_config)
            
html.write_pdf("Report.pdf",stylesheets=[css],
    font_config=font_config)
