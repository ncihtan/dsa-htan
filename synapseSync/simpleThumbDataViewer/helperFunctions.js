const flatten = (obj, roots = [], sep = ".") =>
Object
  // find props of given object
  .keys(obj)
  // return an object by iterating props
  .reduce(
    (memo, prop) =>
      Object.assign(
        // create a new object
        {},
        // include previously returned object
        memo,
        Object.prototype.toString.call(obj[prop]) === "[object Object]"
          ? // keep working if value is an object
            flatten(obj[prop], roots.concat([prop]))
          : // include current prop and value and prefix prop with the roots
            {
              [roots.concat([prop]).join(sep)]: obj[prop],
            }
      ),
    {}
  );

  function smartThumb(obj) {
    $$("groupsChannelList").clearAll();


    $$("thumbSceneImgTwo").parse(obj)
    if (obj.meta.DSAGroupSet && obj.meta.DSAGroupSet.length > 0) {
      console.log(obj.meta.DSAGroupSet);

      var styleInfo = { bands: [] };
      obj.meta.DSAGroupSet[0].channels.forEach((c) => {
        console.table(c);

        styleInfo.bands.push({
          min: c.min,
          max: c.max,
          palette: ["rgb(0,0,0)", c.color],
          frame: c.index,
        });
      });

      obj.thumbGroupStyle = "style=" + JSON.stringify(styleInfo);


      $$("thumbSceneImgTwo").parse(obj)

       $$("groupsChannelList").parse(styleInfo.bands);
       console.log(styleInfo.bands)


    } else {
      obj.thumbStyle = "";
      
    }

    $$("thumbSceneImg").setValues(obj);
  }
