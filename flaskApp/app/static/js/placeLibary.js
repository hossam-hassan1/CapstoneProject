function initAutocomplete() {
    var mapStartingLocation = {lat:38.85637240807301,lng: -90.31152627553638};
    var options = {
      zoom:8,
      center: mapStartingLocation
  }
  // Create map
  var map = new google.maps.Map(document.getElementById('map'),options)
    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
  
    
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
    });
    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
      var places = searchBox.getPlaces();
      if (places.length == 0) {
        return;
      }
      markers = [];
      
      // For each place, get the icon, name and location.
      var bounds = new google.maps.LatLngBounds();
      places.forEach(function(place) {
        if (!place.geometry) {
          console.log("Returned place contains no geometry");
          return;
        }
        var icon = {
          url: place.icon,
          size: new google.maps.Size(71, 71),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(17, 34),
          scaledSize: new google.maps.Size(25, 25)
        };
        
        if (place.geometry.viewport) {
          // Only geocodes have viewport.
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });
      map.fitBounds(bounds);
    });
  
    google.maps.event.addListener(map, 'click', function( event ){
      
      userSelectedMarker = {coords:{lat:event.latLng.lat(), lng:event.latLng.lng()}};
      markersArray.push(userSelectedMarker);
      
      
      // Add markers to the Array
      console.log(markersArray);
      for(var i = 0;i<markersArray.length;i++)
      {
        addMarker(markersArray[i]);
      }
      
    });
    var markersArray = [];
      // empty array
      document.addEventListener("contextmenu", () => {
        markersArray =[];
        
      });
      // Add marker functions
      function addMarker(props)
      {
          var marker = new google.maps.Marker({
               
              position: props.coords,
              // Add markers to this map
              map: map
          });
          
      }
      for(var i = 0;i<markersArray.length;i++)
      {
        addMarker(markersArray[i]);
      }
      // Geolocation
      infoWindow = new google.maps.InfoWindow();
      
      const locationButton = document.createElement("button");
  
      locationButton.textContent = "Pan to Current Location";
      //document.getElementById("locationButton").style.color = "red";
      locationButton.classList.add("custom-map-control-button");
      map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
      locationButton.addEventListener("click", () => {
          // Try HTML5 geolocation.
          if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
              (position) => {
              const pos = {
                  lat: position.coords.latitude,
                  lng: position.coords.longitude,
              };
  
              infoWindow.setPosition(pos);
              infoWindow.setContent("Location found.");
              infoWindow.open(map);
              map.setCenter(pos);
              },
              () => {
              handleLocationError(true, infoWindow, map.getCenter());
              }
          );
          } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
          }
      });
      
  }
  // This function promps the user that location is disabled
  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    window.alert("Location service is disabled")
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation."
    )
  infoWindow.open(map);
  }