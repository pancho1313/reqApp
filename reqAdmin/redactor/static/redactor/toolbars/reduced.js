if (typeof RTOOLBAR == 'undefined') var RTOOLBAR = {};

RTOOLBAR['reduced'] = 
{
	styles:
	{ 
		title: RLANG.styles,
		func: 'show', 				
		dropdown: 
	    {
			 p:
			 {
			 	title: RLANG.paragraph,			 
			 	exec: 'formatblock',
			 	param: '<p>'
			 },
			 h1:
			 {
			 	title: RLANG.header1,			 
			 	exec: 'formatblock',   
			 	param: '<h1>',			 	
			 	style: 'font-size: 30px; line-height: 36px; font-weight: bold;'
			 },
			 h2:
			 {
			 	title: RLANG.header2,			 
			 	exec: 'formatblock',   
			 	param: '<h2>',			 	
			 	style: 'font-size: 24px; line-height: 36px; font-weight: bold;'
			 },
			 h3:
			 {
			 	title: RLANG.header3,			 
			 	exec: 'formatblock', 
			 	param: '<h3>',			 	  
			 	style: 'font-size: 20px; line-height: 30px;  font-weight: bold;'
			 },		
			 h4:
			 {
			 	title: RLANG.header4,			 
			 	exec: 'formatblock', 
			 	param: '<h3>',			 	  
			 	style: 'font-size: 16px; line-height: 26px;  font-weight: bold;'
			 }					 														
		},
		separator: true
	},
	bold:
	{ 
		title: RLANG.bold,
		exec: 'Bold',
	 	param: false	
	}, 
	italic:
	{
		title: RLANG.italic,
		exec: 'italic',
	 	param: null
	},
	deleted:
	{
		title: RLANG.underline,
		exec: 'underline',
	 	param: null,
		separator: true	 		
	},	
	insertunorderedlist:
	{
		title: '&bull; ' + RLANG.unorderedlist,
		exec: 'insertunorderedlist',
	 	param: null
	},
	insertorderedlist:
	{
		title: '1. ' + RLANG.orderedlist,
		exec: 'insertorderedlist',	
	 	param: null
	},
	outdent:
	{
		title: '< ' + RLANG.outdent,
		exec: 'outdent',
	 	param: null		
	},
	indent:
	{
		title: '> ' + RLANG.indent,
		exec: 'indent',
	 	param: null,
		separator: true	 			 			
	},
	justifyleft:
	{	
		exec: 'JustifyLeft', 
		name: 'JustifyLeft', 
		title: RLANG.align_left
	},					
	justifycenter:
	{
		exec: 'JustifyCenter', 
		name: 'JustifyCenter', 
		title: RLANG.align_center
	},
	justifyright: 
	{
		exec: 'JustifyRight', 
		name: 'JustifyRight', 
		title: RLANG.align_right
	},	
	justify: 
	{
		exec: 'justifyfull', 
		name: 'justifyfull', 
		title: RLANG.align_justify, separator: true
	},
	image:
	{
		title: RLANG.image, 						
		func: 'showImage'
	},
};
