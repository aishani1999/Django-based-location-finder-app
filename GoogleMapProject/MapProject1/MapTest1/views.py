import geopy
from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Photon, Nominatim,GoogleV3
from geopy.distance import geodesic
from  .utils import get_geo,get_center_coordinates,get_zoom
import folium


# Create your views here.
def calculate_distance_view(request):
   # device=False;
    obj = get_object_or_404(Measurement,id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Photon(user_agent='measurements')

    ip = '103.87.141.65'
    country, city, lat, lon = get_geo(ip)
    print('location country', country)
    print('location city', city)

    # print('location lat, lon', lat, lon)

    # just to see the location
    location = geolocator.geocode(city)
    print('### location:', location)

    #Location coordinates
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    # Inital Folium map
    m = folium.Map(width=8000, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)

    # Location marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                  icon=folium.Icon(color='red')).add_to(m)


    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        print('destination', destination)

        # Destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)

        # Distance calculation
        distance = round(geodesic(pointA, pointB).km,2)

        # Inital Folium map
        m = folium.Map(width=8000, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distance))

        # Location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                      icon=folium.Icon(color='red')).add_to(m)
       # Destination marker
       # if(device):
        folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
                      icon=folium.Icon(color='green')).add_to(m)
       # else:
        #            folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
         #             icon=folium.Icon(color='red')).add_to(m)

        # Draw line between destination and location
        #line = folium.PolyLine(locations=[pointA,pointB], weight = 2, color= 'blue')
        #m.add_child(line)


        instance.location = location
        instance.distance = distance
        instance.save()

    m= m._repr_html_()

    context = {
        'distance': obj,
        'form' : form,
        'map' : m,
    }

    return render(request,'main.html',context)
