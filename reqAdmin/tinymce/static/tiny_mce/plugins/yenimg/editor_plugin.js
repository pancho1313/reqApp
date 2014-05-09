(function(tinymce) {
	tinymce.create('tinymce.plugins.YenImgPlugin', {
		init : function(ed, url) {

			ed.addButton('imgurl', {
                title : 'Insert Image URL',
                image : url+'/img/img3.png',
                onclick : function() {
                    promptImgURL();
                }
            });
            
            ed.addButton('browseimg', {
                title : 'Insert Image File',
                image : url+'/img/img2.png',
                onclick : function() {}
            });
		},

		getInfo : function() {
			return {
				longname : 'YenImg',
				author : 'Hafon',
				authorurl : '',
				infourl : '',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('yenimg', tinymce.plugins.YenImgPlugin);
})(tinymce);
