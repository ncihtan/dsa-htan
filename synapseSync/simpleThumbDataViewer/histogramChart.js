var histChart = {
    id: "histChart",
    //            height: 400,
    body: {
      view: "form",
      id: "histForm",
      elements: [
        {
          localId: "histogramChart",
          id: "histogramChart",
          view: "chart",
          height: 360,
          width: 630,
          type: "splineArea",
          scale: "logarithmic",
          yValue: "#yValue#",
          color: "#36abee",
          dynamic: false,
          yAxis: {
            template: (yValue) =>
              yValue % 50
                ? ""
                : `<span title='${yValue}' class='y-axis-number-item ellipsis-text'>${yValue}</span>`,
          },
          xAxis: {
            // start: 0,
            // end: 255,
            // step: 0,
            template: function (obj) {
              return obj.binNum % 25
                ? ""
                : `<span title='${Math.floor(obj.xValue)}'>${Math.floor(
                  obj.xValue
                )}</span>`;
            },
            //#"#xValue#"
            // obj => {
            // }
          },
        },
        {
          margin: 5,
          cols: [
            {
              name: "min",
              view: "text",
              label: "min",
            },
            {
              name: "max",
              view: "text",
              label: "max",
            },
          ],
        },
        {
          margin: 5,
          cols: [
            {
              name: "range",
              view: "text",
              label: "range",
            },
            {
              name: "samples",
              view: "text",
              label: "samples",
            },
          ],
        },
      ],
    },
  };
