//**************************************************************************
//* This function is called before default nav filtering is done.
//* If function returns false, default nav filtering happens next.
//* If it returns true, no more nav filtering is done for current keystroke.
//*
//* val is the current content of the nav filter input
//* msg was the initial content of the nav filter input on focus
//**************************************************************************


//***************Additional Enhancements added by Chad Whaley of Fruition Partners***************//
//<nav filter>.<#> = Opens row <#> from the filtered nav options
//<search string>.kb = Searches the Knowledge Base for <search string>
//<search string>.global = Performs a global search for <search string>
//<search string>.wiki = Performs a search for the <search string> in ServiceNow's wiki
//<search string>.google = Performs a google search for <search string>
//<table>.me = Opens the list view of assigned to me
//<table>.active.me = Opens the list view of ACTIVE tickets assigned to me
//<table>.mine = Opens the list view of tickets that I opened
//<table>.active.mine = Opens the list view of ACTIVE tickets that I opened
//<table>:<number>.go = Opens a specific ticket number
//openbs = Opens the background scripts area
//reload = Reloads the main frame
//refresh = Reloads the main frame
//!! = Reloads the main frame
//<number>.find = Looks for a ticket ending with <number>
//<table>.dict = Opens the dictionary list for <table>
//<table>:<encoded query>? = Opens the <table> with the <encoded query> applied as the filter.
//************************************************************************************************//


function navFilterExtension(val, msg) {
    var re1 = '.*?'; // Non-greedy match on filler
    var re2 = '(\\.)'; // Any Single Character 1
    var re3 = '(\\d+)'; // Integer Number 1

    var p = new RegExp(re1 + re2 + re3, ["i"]);
    var m = p.exec(val);

    if (m != null) {
        var links = new Array();
        var c1 = m[1];
        var int1 = m[2];
        var item = c1.replace(/</, "<") + int1.replace(/</, "<");

        var tags = parent.frames['gsft_nav'].document.getElementsByTagName('a');

        //alert(val.replace(item,'') + int1 + " = " + tags[0]);
        for (var i = 0; i < tags.length; i++) {
            if (tags[i].innerText.toString().toLowerCase().startsWith(val.replace(item, '').toLowerCase())) {
                //alert(tags[i].toString());
                links.push(tags[i].toString());
            }
        }

        var server = "${glide.servlet.uri}";
        var url = links[int1 - 1].toString();
        url = url.replace(server, '');
        document.getElementById('gsft_main').src = url;
        restoreFilterText(msg);
        return true;
    }

  if (val.endsWith('.kb')) {
    var qry = val.replace('.kb','');
    qry = qry.replace(' ', '%20');
    var url = "kb_find.do?sysparm_search=" + qry;
    document.getElementById('gsft_main').src = url;
    restoreFilterText(msg);
    return true;
  }

  if (val.endsWith('.global')) {
    var qry = val.replace('.global','');
    qry = qry.replace(' ', '%20');
    var url = "textsearch.do?sysparm_search=" + qry + "&sysparm_recent_search=true";
    document.getElementById('gsft_main').src = url;
    restoreFilterText(msg);
    return true;
  }

  if (val.endsWith('.wiki')) {
    var qry = val.replace('.wiki','');
    qry = qry.replace(' ', '%20');
    var url = "http://wiki.servicenow.com/search-results.php?cx=005409823165138974380%3Abltnnmgfoek&cof=FORID%3A10&ie=UTF-8&q=" + qry + "&sa=Search&siteurl=wiki.servicenow.com%2Findex.php%3Ftitle%3DMain_Page&ref=&ss=415j85491j5";
    window.open(url, '_blank');
    restoreFilterText(msg);
    return true;
  }

  if (val.endsWith('.google')) {
    var qry = val.replace('.google','');
    qry = qry.replace(' ', '%20');
    var url = "https://www.google.com/search?q=" + qry;
    window.open(url, '_blank');
    restoreFilterText(msg);
    return true;
  }

  if (val.endsWith('.me')) {
    var vals = val.split('.');
    //var me = g_user.userID;
    var me = parent.frames["gsft_main"].window.g_user.userID;
    var table = vals[0];
    var url = table + "_list.do?sysparm_query=";
    if(val.indexOf('.active.') != -1) {
       url += "active=true^";
    }
    url += "assigned_to=" + me;
    document.getElementById('gsft_main').src = url;
    restoreFilterText(msg);
    return true;
  }

  if (val.endsWith('.mine')) {
    var vals = val.split('.');
    //var me = g_user.userID;
    var me = parent.frames["gsft_main"].window.g_user.userID;
    var table = vals[0];
    var url = table + "_list.do?sysparm_query=";
    if(val.indexOf('.active.') != -1) {
       url += "active=true^";
    }
    url += "opened_by=" + me;
    document.getElementById('gsft_main').src = url;
    restoreFilterText(msg);
    return true;
  }

  if (val.endsWith('.go')) {
     val = val.replace(/ /g, '');
     var table = val.split(":")[0];
     var record = val.split(":")[1].replace('.go', '');
     document.getElementById('gsft_main').src = table + ".do?sysparm_query=number%3D" + record;
     restoreFilterText(msg);
     return true;
   }
    
   if (val.endsWith('.find')) {
      val = val.replace(/ /g, '');
      var table = 'task';
      var record = val.replace('.find', '');
      document.getElementById('gsft_main').src = table + "_list.do?sysparm_query=numberENDSWITH" + record;
      restoreFilterText(msg);
      return true;
    }

    if (val == 'reload' || val == 'refresh' || val == '!!') {
      document.getElementById('gsft_main').contentWindow.location.reload();
      restoreFilterText(msg);
      return true;
    }

    if (val == 'openbs') {
      document.getElementById('gsft_main').src = "sys.scripts.do";
      restoreFilterText(msg);
      return true;
    }

    if (val.endsWith('.dict')) {
        // example: incident.dict
        // navigates to Dictionary records for the specified table
        val = val.replace(/ /g, '');
        document.getElementById('gsft_main').src = "sys_dictionary_list.do?sysparm_query=name=" + val.replace('.dict', '');
        restoreFilterText(msg);
        return true;
    }

    if (val.endsWith('?')) {
        // example: sys_user:nameLIKEbeth?
        // query specified table using encoded query after the colon
        val = val.replace(/ /g, '');
        var table = val.split(":")[0];
        var query = val.split(":")[1].replace('?', '');
        document.getElementById('gsft_main').src = table + "_list.do?sysparm_query=" + query;
        restoreFilterText(msg);
        return true;
    }

    return false;
}