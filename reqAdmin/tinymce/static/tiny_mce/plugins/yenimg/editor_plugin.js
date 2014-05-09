(function(tinymce) {
	tinymce.create('tinymce.plugins.YenImgPlugin', {
		init : function(ed, url) {

			ed.addButton('imgurl', {
                title : 'image by url',
                image : url+'/img/smiley-cool.gif',
                onclick : function() {
                    promptImgURL();
                }
            });
            
            ed.addButton('browseimg', {
                title : 'browse image file',
                image : url+'/img/smiley-wink.gif',
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
