// add directives to meditationApp
app
.directive('albumSidebar', function() {
    return {
        templateUrl: '/meditation/get-partial-html/sidebar.html'
    };
})
.directive('meditationNavbar', function() {
    return {
        templateUrl: '/meditation/get-partial-html/navbar.html'
    };
})
.directive('activeTooltip', function(){
    return function(scope, element, attrs) {
        $('[data-toggle="tooltip"]').tooltip();
        // if (scope.$last){
        //   // iteration is complete, do whatever post-processing
        //   // is necessary
        //   console.log(scope, element, attrs);
        //   element.parent().css('border', '1px solid black');
        // }
    };
});
