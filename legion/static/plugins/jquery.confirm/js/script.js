$(document).ready(function(){
	
	$('.item .delete').click(function(){
		
		var elem = $(this).closest('.item');
		
		$.confirm({
			'title'		: 'Mensaje de Confirmaci[on',
			'message'	: 'Esta seguro de realizar la acci[on asignada. <br />no podra remediar! Desea Continua?',
			'buttons'	: {
				'Si'	: {
					'class'	: 'blue',
					'action': function(){
						elem.slideUp();
					}
				},
				'No'	: {
					'class'	: 'gray',
					'action': function(){}	// Nothing to do in this case. You can as well omit the action property.
				}
			}
		});
		
	});
	
});