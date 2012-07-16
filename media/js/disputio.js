/* javascript */

$(document).ready(function()
{
	$('#submit-box').hide();
	$('#key-viewer-box').hide();
	
	function new_part(e){
		var nki = $('#new-key-input');
		var keyval = nki.val();
		nki.val('');
		
		var key = $('<div class="part-key">'+keyval+'</div>')
		var value = $('<div class="value-box"><div class="part-value-label">'+keyval+'</div><textarea class="part-value" name="'+keyval+'"></textarea></div>')
		
		$('#new-key-box').append(key);
		$('#edit-box').append(value);
		$('#submit-box').show();
	}
	
	
	$('#new-key-submit').on('click', new_part);
	
	$('#submit-box').on('click', function(e){
		$('#root').submit();
	});
	
	$('#doclist-box').load('/disputio/docs', function(responseText, textStatus, XMLHttpRequest){
		$('.key-item').on('click', function(e){
			that = $(this);
			$('#key-viewer-paper').load(encodeURI(that.attr('title')), function(r,t,x){
				$('#doclist-box').hide();
				$('#key-viewer-box').show();
			});
		});
	});
	
	$('#key-viewer-close').on('click', function(e){
		$('#key-viewer-box').hide();
		$('#doclist-box').show();
	});
	
	
});
