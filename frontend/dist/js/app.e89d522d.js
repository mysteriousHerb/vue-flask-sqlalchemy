(function(e){function t(t){for(var r,o,i=t[0],c=t[1],l=t[2],s=0,d=[];s<i.length;s++)o=i[s],a[o]&&d.push(a[o][0]),a[o]=0;for(r in c)Object.prototype.hasOwnProperty.call(c,r)&&(e[r]=c[r]);f&&f(t);while(d.length)d.shift()();return u.push.apply(u,l||[]),n()}function n(){for(var e,t=0;t<u.length;t++){for(var n=u[t],r=!0,o=1;o<n.length;o++){var i=n[o];0!==a[i]&&(r=!1)}r&&(u.splice(t--,1),e=c(c.s=n[0]))}return e}var r={},o={app:0},a={app:0},u=[];function i(e){return c.p+"js/"+({about:"about"}[e]||e)+"."+{about:"9088ac58"}[e]+".js"}function c(t){if(r[t])return r[t].exports;var n=r[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,c),n.l=!0,n.exports}c.e=function(e){var t=[],n={about:1};o[e]?t.push(o[e]):0!==o[e]&&n[e]&&t.push(o[e]=new Promise(function(t,n){for(var r="css/"+({about:"about"}[e]||e)+"."+{about:"842d190d"}[e]+".css",a=c.p+r,u=document.getElementsByTagName("link"),i=0;i<u.length;i++){var l=u[i],s=l.getAttribute("data-href")||l.getAttribute("href");if("stylesheet"===l.rel&&(s===r||s===a))return t()}var d=document.getElementsByTagName("style");for(i=0;i<d.length;i++){l=d[i],s=l.getAttribute("data-href");if(s===r||s===a)return t()}var f=document.createElement("link");f.rel="stylesheet",f.type="text/css",f.onload=t,f.onerror=function(t){var r=t&&t.target&&t.target.src||a,u=new Error("Loading CSS chunk "+e+" failed.\n("+r+")");u.code="CSS_CHUNK_LOAD_FAILED",u.request=r,delete o[e],f.parentNode.removeChild(f),n(u)},f.href=a;var p=document.getElementsByTagName("head")[0];p.appendChild(f)}).then(function(){o[e]=0}));var r=a[e];if(0!==r)if(r)t.push(r[2]);else{var u=new Promise(function(t,n){r=a[e]=[t,n]});t.push(r[2]=u);var l,s=document.createElement("script");s.charset="utf-8",s.timeout=120,c.nc&&s.setAttribute("nonce",c.nc),s.src=i(e),l=function(t){s.onerror=s.onload=null,clearTimeout(d);var n=a[e];if(0!==n){if(n){var r=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src,u=new Error("Loading chunk "+e+" failed.\n("+r+": "+o+")");u.type=r,u.request=o,n[1](u)}a[e]=void 0}};var d=setTimeout(function(){l({type:"timeout",target:s})},12e4);s.onerror=s.onload=l,document.head.appendChild(s)}return Promise.all(t)},c.m=e,c.c=r,c.d=function(e,t,n){c.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},c.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},c.t=function(e,t){if(1&t&&(e=c(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(c.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)c.d(n,r,function(t){return e[t]}.bind(null,r));return n},c.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return c.d(t,"a",t),t},c.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},c.p="/",c.oe=function(e){throw console.error(e),e};var l=window["webpackJsonp"]=window["webpackJsonp"]||[],s=l.push.bind(l);l.push=t,l=l.slice();for(var d=0;d<l.length;d++)t(l[d]);var f=s;u.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"034f":function(e,t,n){"use strict";var r=n("64a9"),o=n.n(r);o.a},"56d7":function(e,t,n){"use strict";n.r(t);n("cadf"),n("551c"),n("f751"),n("097d");var r=n("2b0e"),o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{attrs:{id:"app"}},[n("v-app",[n("v-navigation-drawer",{attrs:{fixed:"",app:""},model:{value:e.drawer,callback:function(t){e.drawer=t},expression:"drawer"}},[n("v-list",{attrs:{dense:""}},e._l(e.routes,function(t){return n("li",{key:t.id},[n("v-list-tile",{on:{click:function(n){return e.change_view(t.name)}}},[n("v-list-tile-action",[n("v-icon",[e._v(e._s(t.icon))])],1),n("v-list-tile-content",[n("v-list-tile-title",[e._v(e._s(t.name))])],1)],1)],1)}),0)],1),n("v-toolbar",{attrs:{color:"#41B883",dark:"",fixed:"",app:""}},[n("v-toolbar-title",{attrs:{left:""}},[e._v("Application")]),n("v-toolbar-side-icon",{attrs:{left:""},on:{click:function(t){t.stopPropagation(),e.drawer=!e.drawer}}})],1),n("v-content",[n("v-container",[n("router-view")],1)],1),n("v-bottom-nav",{attrs:{active:e.current_view,value:!0,absolute:"",color:"transparent"},on:{"update:active":function(t){e.current_view=t}}},e._l(e.routes,function(t){return n("div",{key:t.id},[n("v-btn",{attrs:{color:"teal",flat:"",value:t.name},on:{click:function(n){return e.change_view(t.name)}}},[n("span",[e._v(e._s(t.name))]),n("v-icon",[e._v(e._s(t.icon))])],1)],1)}),0)],1)],1)},a=[],u={data:function(){return{drawer:!1,routes:[{name:"Home",address:"/",icon:"home"},{name:"About",address:"/about",icon:"person"},{name:"Todo",address:"/todo",icon:"note"}],current_view:"Home"}},mounted:function(){this.change_view(this.current_view)},methods:{change_view:function(e){console.log(e),this.$router.push({name:e}),this.current_view=e}}},i=u,c=(n("034f"),n("2877")),l=Object(c["a"])(i,o,a,!1,null,null,null),s=l.exports,d=n("8c4f");r["default"].use(d["a"]);var f=new d["a"]({mode:"history",base:"/",routes:[{path:"/",name:"Home",component:function(){return n.e("about").then(n.bind(null,"bb51"))}},{path:"/about",name:"About",component:function(){return n.e("about").then(n.bind(null,"f820"))}},{path:"/todo",name:"Todo",component:function(){return n.e("about").then(n.bind(null,"e2a4"))}}]}),p=n("2f62");r["default"].use(p["a"]);var v=new p["a"].Store({state:{},mutations:{},actions:{}}),h=n("bc3a"),m=n.n(h),b=n("ce5b"),g=n.n(b);n("bf40");r["default"].config.productionTip=!1,r["default"].use(g.a),r["default"].prototype.axios=m.a,new r["default"]({router:f,store:v,render:function(e){return e(s)}}).$mount("#app")},"64a9":function(e,t,n){}});
//# sourceMappingURL=app.e89d522d.js.map