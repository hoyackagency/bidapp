var main_module = {
	init: function(){
		
	},
	//--------------Modal module
	open_modal: function(url,modalSize){
		//Open Modal
		$("#main_modal .modal-loader").removeClass('modal-lg').addClass(modalSize)
		$("#main_modal .modal-content").removeClass('modal-lg').addClass(modalSize).load(url,function( response, status, xhr ){
			console.log('test')
			if(status != "error"){
				$("#main_modal").modal('show')
				$("#main_modal").on('hidden.bs.modal', function () {
					$("#main_modal .modal-content").html('');
				})
			}
		});
	},
	close_modal: function(){
		$("#main_modal").modal('hide');
		setTimeout(function(){$("#main_modal .modal-content").html('')},500);
	},
	//Modal Loader
	hide_modal_loader: function(){
		$("#main_modal .modal-loader").hide();
	},
	show_modal_loader: function(){
		$("#main_modal .modal-loader").show();
	},


	//--------------Inner Modal module
	open_inner_modal: function(ele,url,modalSize){
		//Open Modal
		$(ele + " .modal-content").load(url,function( response, status, xhr ){
			console.log(status)
			if(status != "error"){
				$(ele).modal('show')
				$(ele).on('hidden.bs.modal', function () {
					$(ele + " .modal-content").html('');
				});
			}
		});
	},
	//---------------------Ajax Loader Module
	add_ajax_loader: function(element,position){
		if(position=='after'){
			$('<div class="load-bar"><div class="bar"></div><div class="bar"></div><div class="bar"></div></div>').insertAfter(element);
		}else{
			$('<div class="load-bar"><div class="bar"></div><div class="bar"></div><div class="bar"></div></div>').insertBefore(element);
		}
	},
	show_ajax_loader: function(){
		$('.load-bar').show();
	},
	hide_ajax_loader: function(){
		$('.load-bar').hide();
	},
	block: function(){
        $.blockUI({
            baseZ: 2000,
            css: {
                border: 'none',
                padding: '10px',
                backgroundColor: '#000',
                '-webkit-border-radius': '10px',
                '-moz-border-radius': '10px',
                opacity: .5,
                color: '#fff'
            }
        });
	},unblock: function(){
		$.unblockUI();
	}
};
