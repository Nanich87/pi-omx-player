document.querySelectorAll('.ctl').forEach(function (el) {
   el.addEventListener('click', function (e) {
      e.preventDefault();
      el.classList.add('busy');
      fetch(el.href).then(function () {
         if (el.dataset.reload) {
            location.reload();
         }
      }).finally(function () {
         el.classList.remove('busy');
      });
   });
});

var filter = document.getElementById('filter');
filter.addEventListener('input', function () {
   var q = filter.value.trim().toLowerCase();
   var shown = 0;
   document.querySelectorAll('#files .file-item').forEach(function (el) {
      var match = el.dataset.name.indexOf(q) !== -1;
      el.classList.toggle('d-none', !match);
      if (match) {
         shown++;
      }
   });
   var none = document.getElementById('no-match');
   if (none) {
      none.classList.toggle('d-none', shown > 0);
   }
});
