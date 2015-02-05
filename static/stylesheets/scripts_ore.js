$( document ).ready(function() {
	// Call function to setup tabbed nav
	uberNavTabs(
		['ToxInp', 'CropTargetSel', 'OccHandler'],
		{   "isSubTabs":true,
			"ToxInp": [".tab_tox_st", ".tab_tox_it", ".tab_tox_lt"] }
	);

	// Inital setup
	$('.tab_tox_st').show();
	$('.tab_tox_it, .tab_tox_lt, .tab_CropTargetSel, .tab_OccHandler').hide();
	$('#id_expDurationType_0').prop("checked",true);

	// Checkboxes
	var selectedArray = ["id_expDurationType_0"]  // default with Short-term selected
	$("input[name='expDurationType']").click(function() {
		var selection = $(this).attr('id');
		console.log(selection);
		arrayIndex = $.inArray(selection, selectedArray);
		if ( arrayIndex == -1) {
			selectedArray.splice(0, 0, selection);  // add selection to array
			switch(selection) {
				case 'id_expDurationType_0':
					$('.tab_tox_st').show();
					break;
				case 'id_expDurationType_1':
					$('.tab_tox_it').show();
					break;
				case 'id_expDurationType_2':
					$('.tab_tox_lt').show();
					break;
			}
		} else {
			selectedArray.splice(arrayIndex, 1);  // remove selection from array
			switch(selection) {
				case 'id_expDurationType_0':
					$('.tab_tox_st').hide();
					break;
				case 'id_expDurationType_1':
					$('.tab_tox_it').hide();
					break;
				case 'id_expDurationType_2':
					$('.tab_tox_lt').hide();
					break;
			}
		}

	});

	// Crop-Target Lookup
	$('#id_group_no, #id_group_name, #id_subgroup_no, #id_subgroup_name, #id_crop_category').prop('disabled', true);
	var cropTargetFieldsArray = [];
	$('table.tab_CropTargetSel select').each(function() {
		cropTargetFieldsArray.push($(this).attr('id'));
	});
	var noOfCropTargetFields = cropTargetFieldsArray.length;
	$('table.tab_CropTargetSel select').change(function() {
		var curr_crop = $(this).val();
		for (var i = 0; i < noOfCropTargetFields; i++) {
			$('#'+cropTargetFieldsArray[i]).val(curr_crop);
		}
		var value = $('#id_crop_category option:selected').text();
		console.log(value);
		$('#id_exp_category').val(value);
	});
	// $('#id_crop_category').change(function() {
	// 	var value = $(this).text();
	// 	console.log(value);
	// 	$('#id_exp_category').text(value);
	// });

	// NOT FINISHED
	$('.ToxInp').click(function() {
		if ( $.inArray('id_expDurationType_0', selectedArray) !== -1 ) {
			$('.tab_tox_it, .tab_tox_lt').hide();
			$('.tab_tox_st').show();
		} else if ( $.inArray('id_expDurationType_1', selectedArray) !== -1 ) {
			$('.tab_tox_st, .tab_tox_lt').hide();
			$('.tab_tox_it').show();
		} else if ( $.inArray('id_expDurationType_2', selectedArray) !== -1 ) {
			$('.tab_tox_st, .tab_tox_it').hide();
			$('.tab_tox_lt').show();
		}
	});

	// Enabled Crop-Target Category Lookup form fields before form submit
	// ***Not needed with how the fields are populated currently; must re-query DB after form submit***
	// $('.submit').click(function(e) {
	// 	e.preventDefault();
	// 	alert('Prevented!');
	// 	$('#id_group_no, #id_group_name, #id_subgroup_no, #id_subgroup_name, #id_crop_category').prop('disabled', false);
	// 	$('form').submit();
	// });

});