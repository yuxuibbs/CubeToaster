startHTML = '''
  <html>
    <head>
      <link rel="stylesheet" type="text/css" href="screen.css" />
    </head>
    <body>
'''

ao5Table = '''
      <table>
        <tr>
          <th colspan="6" class="compName">competitionName</th>
        </tr>
        <tr>
          <th colspan="1" class="personID">competitorID</th>
          <th colspan="3" class="event">eventName</th>
          <th colspan="1" class="heat">Heat: heatNumber</th>
          <th colspan="1" class="round">Round: roundNumber</th>
        </tr>
        <tr>
          <th colspan="6" class="personName">competitorName</th>
        </tr>
        <tr class="labels">
          <th colspan="1"> </th>
          <th colspan="3">Results</th>
          <th colspan="1" class="initial">Comp</th>
          <th colspan="1" class="initial">Judge</th>
        </tr>
        <tr class="attempt">
          <td colspan="1">1</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1">2</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="cutoffs">
          <td colspan="1"></td>
          <td colspan="1">Soft Cutoff: softCutoff</td>
          <td colspan="1"></td>
          <td colspan="1">Time Limit: timeLimit</td>
          <td colspan="1"></td>
          <td colspan="1"></td>
        </tr>
        <tr class="attempt">
          <td colspan="1">3</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1">4</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1">5</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="empty">
          <td colspan="6"></td>
        </tr>
        <tr class="attempt">
          <td colspan="1">6</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
      </table>
'''


mo3Table = '''
      <table>
        <tr>
          <th colspan="6" class="compName">competitionName</th>
        </tr>
        <tr>
          <th colspan="1" class="personID">competitorID</th>
          <th colspan="3" class="event">eventName</th>
          <th colspan="1" class="heat">Heat: heatNumber</th>
          <th colspan="1" class="round">Round: roundNumber</th>
        </tr>
        <tr>
          <th colspan="6" class="personName">competitorName</th>
        </tr>
        <tr class="labels">
          <th colspan="1"> </th>
          <th colspan="3">Results</th>
          <th colspan="1" class="initial">Comp</th>
          <th colspan="1" class="initial">Judge</th>
        </tr>
        <tr class="attempt">
          <td colspan="1">1</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="cutoffs">
          <td colspan="1"></td>
          <td colspan="1">Soft Cutoff: softCutoff</td>
          <td colspan="1"></td>
          <td colspan="1">Time Limit: timeLimit</td>
          <td colspan="1"></td>
          <td colspan="1"></td>
        <tr class="attempt">
          <td colspan="1">2</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1">3</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="empty">
          <td colspan="6"></td>
        </tr>
        <tr class="attempt">
          <td colspan="1">4</td>
          <td colspan="3"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
      </table>
'''


endHTML = '''
    </body>
  </html>
'''