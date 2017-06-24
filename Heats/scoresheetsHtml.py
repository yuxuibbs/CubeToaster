startHTML = '''
  <html>
    <head>
      <style>
        table {
          border-collapse: collapse;
          height: 100%;
          width: 100%;
        }
        table, th, td {
          border: 3px solid black;
        }
        @media print {
          table {
            page-break-after: always;
          }
        }
        .cutoffs td {
          border: 0;
          font-weight: bold;
        }
        .compName {
          font-size: 48pt;
          font-weight: bold;
        }
        .labels {
          font-size: 24pt;
          font-weight: bold;
        }
        .attempt {
          font-size: 36pt;
          font-weight: bold;
          text-align: center;
        }
        .event, .personID {
          font-size: 24pt;
          font-weight: bold;
          width: 60px;
        }
        .round, .heat {
          font-size: 24pt;
          font-weight: bold;
        }
        .personName {
          font-size: 40pt;
          font-weight: bold;
        }
        .initial {
          width: 120px;
        }
      </style>
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
          <th colspan="1" class="heat">G: heatNumber</th>
          <th colspan="1" class="round">R: roundNumber</th>
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
          <td colspan="1">Cutoff: cutoffTime</td>
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
          <th colspan="1" class="heat">G: heatNumber</th>
          <th colspan="1" class="round">R: roundNumber</th>
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
          <td colspan="1">Cutoff: cutoffTime</td>
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