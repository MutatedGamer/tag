	// Image cropping jQuery
    $(function () {
      /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
      $(".photo").change(function () {

        if (this.files && this.files[0]) {
          var reader = new FileReader();
		  $(this).closest('.modal-body').addClass('cropping');
          reader.onload = function (e) {
            $("#image").attr("src", e.target.result);
            $("#modalCrop").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
      });

      /* SCRIPTS TO HANDLE THE CROPPER BOX */
      var $image = $("#image");
      var cropBoxData;
      var canvasData;
      $("#modalCrop").on("shown.bs.modal", function () {
        $image.cropper({
          viewMode: 1,
          aspectRatio: 1/1,
          minCropBoxWidth: 100,
          minCropBoxHeight: 100,
          ready: function () {
            $image.cropper("setCanvasData", canvasData);
            $image.cropper("setCropBoxData", cropBoxData);
          }
        });
      }).on("hidden.bs.modal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
		var croppingForm = $('.cropping');
		croppingForm.removeClass('cropping');
      });

      $(".js-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
      });

      $(".js-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
      });

      /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
      $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
		var croppingForm = $('.cropping');
        croppingForm.find("#id_x").val(cropData["x"]);
        croppingForm.find("#id_y").val(cropData["y"]);
        croppingForm.find("#id_height").val(cropData["height"]);
        croppingForm.find("#id_width").val(cropData["width"]);
		$('#modalCrop').modal('hide');
		croppingForm.removeClass('cropping');
		if (croppingForm.hasClass('update-profile')) {
			var canvas = $image.cropper('getCroppedCanvas');
			var image = new Image();
			$('#imagePreview').css('background-image', 'url(' + canvas.toDataURL() + ')');
		};
      });

	  $('.close-crop').click(function () {
		var croppingForm = $('.cropping');
		croppingForm.removeClass('cropping');
	  });


    });

