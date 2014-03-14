/*  Sonrisatroll
    Aplicación: Sonrisatroll Widgets
    Aplicación URL: http://www.sonrisatroll.com
    Autor: José Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
    Requiere jQuery 1.9.1
*/
function loadSocial(){if($(".twitter-share-button").length==0)return false;if(typeof twttr!="undefined"){twttr.widgets.load()}else{$.getScript("http://platform.twitter.com/widgets.js")}if(typeof FB!="undefined"){FB.init({status:true,cookie:true,xfbml:true})}else{$.getScript("http://connect.facebook.net/es_ES/all.js#xfbml=1",function(){FB.init({status:true,cookie:true,xfbml:true})})}if(typeof gapi!="undefined"){$(".g-plusone").each(function(){gapi.plusone.render($(this).get(0))})}else{$.getScript("http://apis.google.com/js/plusone.js")}}$(window).load(function(){loadSocial()});(function(e,t,n){var r,i=t.getElementsByTagName("SCRIPT")[0],s=n.length,o=0,u=function(){for(o=0;o<s;o=o+1){r=t.createElement("SCRIPT");r.type="text/javascript";r.async=true;r.src=n[o];i.parentNode.insertBefore(r,i)}};if(e.attachEvent){e.attachEvent("onload",u)}else{e.addEventListener("load",u,false)}})(window,document,["http://assets.pinterest.com/js/pinit.js"])