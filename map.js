    
    
            var map_9eb96eb1fe9bc3ea56b51a20c1cf6a00 = L.map(
                "map_9eb96eb1fe9bc3ea56b51a20c1cf6a00",
                {
                    center: [42.9, -75.0],
                    crs: L.CRS.EPSG3857,
                    zoom: 7,
                    zoomControl: true,
                    preferCanvas: false,
                }
            );

            

        
    
            var tile_layer_04c0d540e422a0223c0c65ed3a113aae = L.tileLayer(
                "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
                {"attribution": "\u0026copy; \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eOpenStreetMap\u003c/a\u003e contributors \u0026copy; \u003ca href=\"http://cartodb.com/attributions\"\u003eCartoDB\u003c/a\u003e, CartoDB \u003ca href =\"http://cartodb.com/attributions\"\u003eattributions\u003c/a\u003e", "detectRetina": false, "maxNativeZoom": 18, "maxZoom": 18, "minZoom": 0, "noWrap": false, "opacity": 1, "subdomains": "abc", "tms": false}
            ).addTo(map_9eb96eb1fe9bc3ea56b51a20c1cf6a00);
        
    
            L.control.fullscreen(
                {"forceSeparateButton": false, "position": "topleft", "title": "Full Screen", "titleCancel": "Exit Full Screen"}
            ).addTo(map_9eb96eb1fe9bc3ea56b51a20c1cf6a00);
        
    
            var feature_group_3983efa59c3fa7675054fceade5a1d6a = L.featureGroup(
                {}
            ).addTo(map_9eb96eb1fe9bc3ea56b51a20c1cf6a00);
        
    
            var polygon_d618b697f7f8fcc095d03a26b5f6ce9a = L.polygon(
                [[44.33, -74.06], [44.38, -73.91], [44.31, -73.74], [44.18, -73.66], [44.06, -73.8], [44.03, -74.02], [44.13, -74.16], [44.27, -74.13]],
                {"bubblingMouseEvents": true, "color": "#c83737", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#c83737", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_d618b697f7f8fcc095d03a26b5f6ce9a.bindTooltip(
                `<div>
                     Adirondack High Peaks (Keene/Keene Valley, Lake Placid) (Score 10.0) - 5h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_77eebcfc0860bf21e034596f6543c032 = L.polygon(
                [[43.58, -73.82], [43.61, -73.66], [43.55, -73.48], [43.38, -73.45], [43.29, -73.56], [43.31, -73.78], [43.45, -73.87]],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_77eebcfc0860bf21e034596f6543c032.bindTooltip(
                `<div>
                     Lake George & Pharaoh Lake Wilderness (Score 8.5) - 3h 48m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_d937f6238946556e76544e3f0991a074 = L.polygon(
                [[42.23, -74.68], [42.2, -74.39], [42.11, -74.06], [41.92, -74.21], [41.88, -74.55], [42.0, -74.74], [42.13, -74.76]],
                {"bubblingMouseEvents": true, "color": "#c83737", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#c83737", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_d937f6238946556e76544e3f0991a074.bindTooltip(
                `<div>
                     Catskills (Slide, Hunter, Kaaterskill) (Score 9.2) - 2h 30m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_fe24b94d3aa330b19a1ccade13bed7fd = L.polygon(
                [[41.85, -74.08], [41.81, -74.16], [41.76, -74.23], [41.72, -74.28], [41.68, -74.35], [41.65, -74.39], [41.62, -74.33], [41.65, -74.22], [41.69, -74.13], [41.77, -74.03], [41.82, -73.99]],
                {"bubblingMouseEvents": true, "color": "#e06b2e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#e06b2e", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_fe24b94d3aa330b19a1ccade13bed7fd.bindTooltip(
                `<div>
                     Shawangunks / Minnewaska & Mohonk Preserve (Score 8.8) - 2h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_717409ba12259baf908aaa4294d3f96c = L.polygon(
                [[41.53, -73.99], [41.5, -73.94], [41.47, -73.92], [41.43, -73.94], [41.41, -73.99], [41.43, -74.05], [41.48, -74.06], [41.52, -74.02]],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_717409ba12259baf908aaa4294d3f96c.bindTooltip(
                `<div>
                     Hudson Highlands (Breakneck, Storm King, Bull Hill) (Score 8.6) - 1h 18m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_6e35accc2281c367b9a478b4b47e48a6 = L.polygon(
                [[41.41, -73.86], [41.34, -73.9], [41.3, -73.97], [41.28, -74.06], [41.23, -74.17], [41.19, -74.22], [41.25, -74.26], [41.33, -74.21], [41.38, -74.1], [41.41, -73.98]],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_6e35accc2281c367b9a478b4b47e48a6.bindTooltip(
                `<div>
                     Harriman–Bear Mountain State Parks (Score 8.0) - 1h 06m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_5b1714e894484b5539a8b90eca2e91de = L.polygon(
                [[42.55, -76.58], [42.54, -76.47], [42.52, -76.4], [42.45, -76.35], [42.38, -76.4], [42.35, -76.5], [42.38, -76.61], [42.47, -76.65]],
                {"bubblingMouseEvents": true, "color": "#e06b2e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#e06b2e", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_5b1714e894484b5539a8b90eca2e91de.bindTooltip(
                `<div>
                     Finger Lakes Gorges (Ithaca area) (Score 8.9) - 4h 12m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_48532906570b72625b4ba10c94c47d7a = L.polygon(
                [[42.43, -76.99], [42.41, -76.94], [42.39, -76.88], [42.36, -76.85], [42.33, -76.88], [42.32, -76.95], [42.35, -77.0], [42.39, -77.02]],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_48532906570b72625b4ba10c94c47d7a.bindTooltip(
                `<div>
                     Watkins Glen & Surrounds (Score 8.4) - 4h 30m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_a5549700300c4a1172aa3a0436735c68 = L.polygon(
                [[42.74, -78.13], [42.71, -78.07], [42.67, -78.02], [42.63, -77.94], [42.6, -77.96], [42.58, -78.02], [42.61, -78.11], [42.67, -78.15]],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_a5549700300c4a1172aa3a0436735c68.bindTooltip(
                `<div>
                     Letchworth State Park (Genesee River Gorge) (Score 8.7) - 6h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_113d89c68a3c21335347e67742988b13 = L.polygon(
                [[42.21, -78.92], [42.16, -78.95], [42.08, -78.9], [41.99, -78.82], [42.0, -78.64], [42.11, -78.58], [42.2, -78.73], [42.23, -78.85]],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_113d89c68a3c21335347e67742988b13.bindTooltip(
                `<div>
                     Allegany State Park (Southern Tier) (Score 7.8) - 7h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_b3dec9d3a51a7246559bb055da3881d9 = L.polygon(
                [[43.18, -79.06], [43.15, -79.06], [43.12, -79.04], [43.1, -79.02], [43.08, -78.99], [43.12, -78.98], [43.16, -79.0], [43.18, -79.02]],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_b3dec9d3a51a7246559bb055da3881d9.bindTooltip(
                `<div>
                     Niagara Gorge (NY side) (Score 8.2) - 6h 48m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_c6a859a0005ffafdffeebe312b0250fc = L.polygon(
                [[42.2, -73.6], [42.17, -73.52], [42.13, -73.45], [42.05, -73.36], [41.97, -73.4], [41.95, -73.55], [42.02, -73.62], [42.1, -73.64]],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_c6a859a0005ffafdffeebe312b0250fc.bindTooltip(
                `<div>
                     Taconic Range / Harlem Valley (incl. Bash Bish area) (Score 8.1) - 2h 18m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_d6c226c67500597c3deeaf8b3c75e3a3 = L.polygon(
                [[41.12, -71.94], [41.1, -71.92], [41.05, -71.91], [41.03, -71.88], [41.03, -71.8], [41.07, -71.8], [41.1, -71.83], [41.12, -71.88]],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_d6c226c67500597c3deeaf8b3c75e3a3.bindTooltip(
                `<div>
                     Long Island North & South Fork highlights (Montauk bluffs) (Score 7.5) - 3h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var polygon_d77fe48f038caf5929da693749f287d2 = L.polygon(
                [[40.97, -73.49], [40.95, -73.5], [40.92, -73.47], [40.91, -73.44], [40.93, -73.41], [40.96, -73.42]],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.18, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 2}
            ).addTo(feature_group_3983efa59c3fa7675054fceade5a1d6a);
        
    
            polygon_d77fe48f038caf5929da693749f287d2.bindTooltip(
                `<div>
                     Caumsett State Historic Park Preserve (Lloyd Neck) (Score 7.2) - 1h 18m
                 </div>`,
                {"sticky": true}
            );
        
    
            var feature_group_045a5715d02866a8d3ae3f29fb7b4703 = L.featureGroup(
                {}
            ).addTo(map_9eb96eb1fe9bc3ea56b51a20c1cf6a00);
        
    
            var circle_marker_7f2758b4fe2e0184d5f62ec43e78b451 = L.circleMarker(
                [44.15, -73.86],
                {"bubblingMouseEvents": true, "color": "#c83737", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#c83737", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_f3677bbcea19529144116660c6340bd1 = L.popup({"maxWidth": 360});

        
            var html_c0091821176f03064c351a42601c7aaa = $(`<div id="html_c0091821176f03064c351a42601c7aaa" style="width: 100.0%; height: 100.0%;"><b>Adirondack High Peaks (Keene/Keene Valley, Lake Placid)</b><br>     Scenery/Hiking Score: 10 / 10<br>     Drive time from NYC (off‑peak): <b>5h 00m</b><br>     <i>46 High Peaks • alpine zones • Avalanche Pass, Marcy, Gothics</i></div>`)[0];
            popup_f3677bbcea19529144116660c6340bd1.setContent(html_c0091821176f03064c351a42601c7aaa);
        

        circle_marker_7f2758b4fe2e0184d5f62ec43e78b451.bindPopup(popup_f3677bbcea19529144116660c6340bd1)
        ;

        
    
    
            circle_marker_7f2758b4fe2e0184d5f62ec43e78b451.bindTooltip(
                `<div>
                     Adirondack High Peaks (Keene/Keene Valley, Lake Placid)
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_30b8a316ac100a32c6558a20a2376227 = L.circleMarker(
                [43.42, -73.71],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_044f4aeff8ccb2bcc021d7b3f298b210 = L.popup({"maxWidth": 360});

        
            var html_295e7dc1428cb0cbf9ed5358bb8425a5 = $(`<div id="html_295e7dc1428cb0cbf9ed5358bb8425a5" style="width: 100.0%; height: 100.0%;"><b>Lake George & Pharaoh Lake Wilderness</b><br>     Scenery/Hiking Score: 8.5 / 10<br>     Drive time from NYC (off‑peak): <b>3h 48m</b><br>     <i>Ridge walks • island views • Tongue Mountain Range</i></div>`)[0];
            popup_044f4aeff8ccb2bcc021d7b3f298b210.setContent(html_295e7dc1428cb0cbf9ed5358bb8425a5);
        

        circle_marker_30b8a316ac100a32c6558a20a2376227.bindPopup(popup_044f4aeff8ccb2bcc021d7b3f298b210)
        ;

        
    
    
            circle_marker_30b8a316ac100a32c6558a20a2376227.bindTooltip(
                `<div>
                     Lake George & Pharaoh Lake Wilderness
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_690d82b4a0e84e4f6d62a99024af343d = L.circleMarker(
                [42.03, -74.4],
                {"bubblingMouseEvents": true, "color": "#c83737", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#c83737", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_a20a97ebb1ecb2a56e84e93ddfdbf258 = L.popup({"maxWidth": 360});

        
            var html_0f27a9812e697f52156afcc058500247 = $(`<div id="html_0f27a9812e697f52156afcc058500247" style="width: 100.0%; height: 100.0%;"><b>Catskills (Slide, Hunter, Kaaterskill)</b><br>     Scenery/Hiking Score: 9.2 / 10<br>     Drive time from NYC (off‑peak): <b>2h 30m</b><br>     <i>Classic Northeast peaks • Spruce-fir summits • waterfalls</i></div>`)[0];
            popup_a20a97ebb1ecb2a56e84e93ddfdbf258.setContent(html_0f27a9812e697f52156afcc058500247);
        

        circle_marker_690d82b4a0e84e4f6d62a99024af343d.bindPopup(popup_a20a97ebb1ecb2a56e84e93ddfdbf258)
        ;

        
    
    
            circle_marker_690d82b4a0e84e4f6d62a99024af343d.bindTooltip(
                `<div>
                     Catskills (Slide, Hunter, Kaaterskill)
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_813431bee295e856966e43e199342cac = L.circleMarker(
                [41.73, -74.22],
                {"bubblingMouseEvents": true, "color": "#e06b2e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#e06b2e", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_83c6330690be2309f5d9c7a6fdcd54bd = L.popup({"maxWidth": 360});

        
            var html_242951bf064611cc46e2eb8ef2f3072c = $(`<div id="html_242951bf064611cc46e2eb8ef2f3072c" style="width: 100.0%; height: 100.0%;"><b>Shawangunks / Minnewaska & Mohonk Preserve</b><br>     Scenery/Hiking Score: 8.8 / 10<br>     Drive time from NYC (off‑peak): <b>2h 00m</b><br>     <i>Sky lakes • white cliffs • carriage roads & scrambles</i></div>`)[0];
            popup_83c6330690be2309f5d9c7a6fdcd54bd.setContent(html_242951bf064611cc46e2eb8ef2f3072c);
        

        circle_marker_813431bee295e856966e43e199342cac.bindPopup(popup_83c6330690be2309f5d9c7a6fdcd54bd)
        ;

        
    
    
            circle_marker_813431bee295e856966e43e199342cac.bindTooltip(
                `<div>
                     Shawangunks / Minnewaska & Mohonk Preserve
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_42b53b3e7dad19fbe4f9bcd69b86bd7c = L.circleMarker(
                [41.45, -73.98],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_9a1436b1bc4d3e875e8f29efb72fc1f2 = L.popup({"maxWidth": 360});

        
            var html_61acad990b518fa233f43a8cd6312212 = $(`<div id="html_61acad990b518fa233f43a8cd6312212" style="width: 100.0%; height: 100.0%;"><b>Hudson Highlands (Breakneck, Storm King, Bull Hill)</b><br>     Scenery/Hiking Score: 8.6 / 10<br>     Drive time from NYC (off‑peak): <b>1h 18m</b><br>     <i>River panoramas • steep but short classics • train-access options</i></div>`)[0];
            popup_9a1436b1bc4d3e875e8f29efb72fc1f2.setContent(html_61acad990b518fa233f43a8cd6312212);
        

        circle_marker_42b53b3e7dad19fbe4f9bcd69b86bd7c.bindPopup(popup_9a1436b1bc4d3e875e8f29efb72fc1f2)
        ;

        
    
    
            circle_marker_42b53b3e7dad19fbe4f9bcd69b86bd7c.bindTooltip(
                `<div>
                     Hudson Highlands (Breakneck, Storm King, Bull Hill)
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_dc503b27be8f88dda948bcd1f8230c83 = L.circleMarker(
                [41.31, -74.02],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_36860d316f762876ecddee02e7e27bf9 = L.popup({"maxWidth": 360});

        
            var html_c89f1b3655822649919d4e5632ce893a = $(`<div id="html_c89f1b3655822649919d4e5632ce893a" style="width: 100.0%; height: 100.0%;"><b>Harriman–Bear Mountain State Parks</b><br>     Scenery/Hiking Score: 8.0 / 10<br>     Drive time from NYC (off‑peak): <b>1h 06m</b><br>     <i>Hundreds of miles of trails • lakes • Appalachian Trail segments</i></div>`)[0];
            popup_36860d316f762876ecddee02e7e27bf9.setContent(html_c89f1b3655822649919d4e5632ce893a);
        

        circle_marker_dc503b27be8f88dda948bcd1f8230c83.bindPopup(popup_36860d316f762876ecddee02e7e27bf9)
        ;

        
    
    
            circle_marker_dc503b27be8f88dda948bcd1f8230c83.bindTooltip(
                `<div>
                     Harriman–Bear Mountain State Parks
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_fa183ebe0c7c8054512e5c6e264d1908 = L.circleMarker(
                [42.44, -76.5],
                {"bubblingMouseEvents": true, "color": "#e06b2e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#e06b2e", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_0d9e87738a0e88fab807229ae6abfdbe = L.popup({"maxWidth": 360});

        
            var html_97f7a0d5465957267174977222cb282f = $(`<div id="html_97f7a0d5465957267174977222cb282f" style="width: 100.0%; height: 100.0%;"><b>Finger Lakes Gorges (Ithaca area)</b><br>     Scenery/Hiking Score: 8.9 / 10<br>     Drive time from NYC (off‑peak): <b>4h 12m</b><br>     <i>Stone-cut gorges • rim trails • waterfalls (Treman, Buttermilk, Taughannock)</i></div>`)[0];
            popup_0d9e87738a0e88fab807229ae6abfdbe.setContent(html_97f7a0d5465957267174977222cb282f);
        

        circle_marker_fa183ebe0c7c8054512e5c6e264d1908.bindPopup(popup_0d9e87738a0e88fab807229ae6abfdbe)
        ;

        
    
    
            circle_marker_fa183ebe0c7c8054512e5c6e264d1908.bindTooltip(
                `<div>
                     Finger Lakes Gorges (Ithaca area)
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_5d6c10afd0f0a9d7068b152fb6981892 = L.circleMarker(
                [42.37, -76.88],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_820aad0860ec79a72e6b5fc88ac88733 = L.popup({"maxWidth": 360});

        
            var html_7d1def34608b5479a4ac8ae73605affb = $(`<div id="html_7d1def34608b5479a4ac8ae73605affb" style="width: 100.0%; height: 100.0%;"><b>Watkins Glen & Surrounds</b><br>     Scenery/Hiking Score: 8.4 / 10<br>     Drive time from NYC (off‑peak): <b>4h 30m</b><br>     <i>Iconic gorge • stairways & bridges • Seneca Lake views</i></div>`)[0];
            popup_820aad0860ec79a72e6b5fc88ac88733.setContent(html_7d1def34608b5479a4ac8ae73605affb);
        

        circle_marker_5d6c10afd0f0a9d7068b152fb6981892.bindPopup(popup_820aad0860ec79a72e6b5fc88ac88733)
        ;

        
    
    
            circle_marker_5d6c10afd0f0a9d7068b152fb6981892.bindTooltip(
                `<div>
                     Watkins Glen & Surrounds
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_e6c9ddd61e38428f81cbb30038a82c03 = L.circleMarker(
                [42.65, -77.95],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_953a916fed89436ed6c962a29276cc73 = L.popup({"maxWidth": 360});

        
            var html_71e8cd4a5524a4cf84445cd98f29e513 = $(`<div id="html_71e8cd4a5524a4cf84445cd98f29e513" style="width: 100.0%; height: 100.0%;"><b>Letchworth State Park (Genesee River Gorge)</b><br>     Scenery/Hiking Score: 8.7 / 10<br>     Drive time from NYC (off‑peak): <b>6h 00m</b><br>     <i>‘Grand Canyon of the East’ • three major falls • rim trails</i></div>`)[0];
            popup_953a916fed89436ed6c962a29276cc73.setContent(html_71e8cd4a5524a4cf84445cd98f29e513);
        

        circle_marker_e6c9ddd61e38428f81cbb30038a82c03.bindPopup(popup_953a916fed89436ed6c962a29276cc73)
        ;

        
    
    
            circle_marker_e6c9ddd61e38428f81cbb30038a82c03.bindTooltip(
                `<div>
                     Letchworth State Park (Genesee River Gorge)
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_dee68a2c31427299b52a29aa04f3a6b4 = L.circleMarker(
                [42.09, -78.75],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_669b5586472e09db6faa0f24fab70311 = L.popup({"maxWidth": 360});

        
            var html_4265d90911a42bca8ce669481bc6928a = $(`<div id="html_4265d90911a42bca8ce669481bc6928a" style="width: 100.0%; height: 100.0%;"><b>Allegany State Park (Southern Tier)</b><br>     Scenery/Hiking Score: 7.8 / 10<br>     Drive time from NYC (off‑peak): <b>7h 00m</b><br>     <i>Remote feel • rolling ridges • long multi-hour loops</i></div>`)[0];
            popup_669b5586472e09db6faa0f24fab70311.setContent(html_4265d90911a42bca8ce669481bc6928a);
        

        circle_marker_dee68a2c31427299b52a29aa04f3a6b4.bindPopup(popup_669b5586472e09db6faa0f24fab70311)
        ;

        
    
    
            circle_marker_dee68a2c31427299b52a29aa04f3a6b4.bindTooltip(
                `<div>
                     Allegany State Park (Southern Tier)
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_45683b5827a0ce5a97c1f0ef280b71a0 = L.circleMarker(
                [43.12, -79.05],
                {"bubblingMouseEvents": true, "color": "#d6a62e", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#d6a62e", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_bde826e75b08dc345cd8726838a7e518 = L.popup({"maxWidth": 360});

        
            var html_2d9225f6c2f630f89e20a2b780927fc0 = $(`<div id="html_2d9225f6c2f630f89e20a2b780927fc0" style="width: 100.0%; height: 100.0%;"><b>Niagara Gorge (NY side)</b><br>     Scenery/Hiking Score: 8.2 / 10<br>     Drive time from NYC (off‑peak): <b>6h 48m</b><br>     <i>Dramatic river gorge • whirlpool rapids • rim & gorge trails</i></div>`)[0];
            popup_bde826e75b08dc345cd8726838a7e518.setContent(html_2d9225f6c2f630f89e20a2b780927fc0);
        

        circle_marker_45683b5827a0ce5a97c1f0ef280b71a0.bindPopup(popup_bde826e75b08dc345cd8726838a7e518)
        ;

        
    
    
            circle_marker_45683b5827a0ce5a97c1f0ef280b71a0.bindTooltip(
                `<div>
                     Niagara Gorge (NY side)
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_5ae612d9ca49c40ea05dae4b6361ca9c = L.circleMarker(
                [42.09, -73.48],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_2bf808b85cf5977e5a18d28503f32492 = L.popup({"maxWidth": 360});

        
            var html_840742181a58a925552d6d328e1be57d = $(`<div id="html_840742181a58a925552d6d328e1be57d" style="width: 100.0%; height: 100.0%;"><b>Taconic Range / Harlem Valley (incl. Bash Bish area)</b><br>     Scenery/Hiking Score: 8.1 / 10<br>     Drive time from NYC (off‑peak): <b>2h 18m</b><br>     <i>Ridgetop views • state-line loop options • Bash Bish Falls nearby</i></div>`)[0];
            popup_2bf808b85cf5977e5a18d28503f32492.setContent(html_840742181a58a925552d6d328e1be57d);
        

        circle_marker_5ae612d9ca49c40ea05dae4b6361ca9c.bindPopup(popup_2bf808b85cf5977e5a18d28503f32492)
        ;

        
    
    
            circle_marker_5ae612d9ca49c40ea05dae4b6361ca9c.bindTooltip(
                `<div>
                     Taconic Range / Harlem Valley (incl. Bash Bish area)
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_7e01508fb18093da6cc86abd812ee6d2 = L.circleMarker(
                [41.03, -71.94],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_9a2e23b7c32ae36723ec9f9a9d70da5d = L.popup({"maxWidth": 360});

        
            var html_cef49eda6da412d5e6b237821427f6be = $(`<div id="html_cef49eda6da412d5e6b237821427f6be" style="width: 100.0%; height: 100.0%;"><b>Long Island North & South Fork highlights (Montauk bluffs)</b><br>     Scenery/Hiking Score: 7.5 / 10<br>     Drive time from NYC (off‑peak): <b>3h 00m</b><br>     <i>Coastal bluffs • dune walks • lighthouse views • shoulder-season gems</i></div>`)[0];
            popup_9a2e23b7c32ae36723ec9f9a9d70da5d.setContent(html_cef49eda6da412d5e6b237821427f6be);
        

        circle_marker_7e01508fb18093da6cc86abd812ee6d2.bindPopup(popup_9a2e23b7c32ae36723ec9f9a9d70da5d)
        ;

        
    
    
            circle_marker_7e01508fb18093da6cc86abd812ee6d2.bindTooltip(
                `<div>
                     Long Island North & South Fork highlights (Montauk bluffs)
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_f8357a23b9417756631e88735f463128 = L.circleMarker(
                [40.93, -73.46],
                {"bubblingMouseEvents": true, "color": "#7cb342", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#7cb342", "fillOpacity": 0.9, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 7, "stroke": true, "weight": 3}
            ).addTo(feature_group_045a5715d02866a8d3ae3f29fb7b4703);
        
    
        var popup_157a33f031fcfe38fd10aa112e6c552a = L.popup({"maxWidth": 360});

        
            var html_070de2d4ada106de58539997d52ace15 = $(`<div id="html_070de2d4ada106de58539997d52ace15" style="width: 100.0%; height: 100.0%;"><b>Caumsett State Historic Park Preserve (Lloyd Neck)</b><br>     Scenery/Hiking Score: 7.2 / 10<br>     Drive time from NYC (off‑peak): <b>1h 18m</b><br>     <i>Easy coastal loops • meadow & shoreline scenery • family friendly</i></div>`)[0];
            popup_157a33f031fcfe38fd10aa112e6c552a.setContent(html_070de2d4ada106de58539997d52ace15);
        

        circle_marker_f8357a23b9417756631e88735f463128.bindPopup(popup_157a33f031fcfe38fd10aa112e6c552a)
        ;

        
    
    
            circle_marker_f8357a23b9417756631e88735f463128.bindTooltip(
                `<div>
                     Caumsett State Historic Park Preserve (Lloyd Neck)
                 </div>`,
                {"sticky": true}
            );
        
    
            var feature_group_dacbddd05370aa53667cdcd0d78eedbe = L.featureGroup(
                {}
            ).addTo(map_9eb96eb1fe9bc3ea56b51a20c1cf6a00);
        
    
            var circle_marker_009c049a4e02003d7ba29c098de96be1 = L.circleMarker(
                [44.28, -73.98],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.8781438859330635, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_288b50afd9b21105971c77f7796f23ba = L.popup({"maxWidth": 260});

        
            var html_cb06267ad3b164f9c11b11a5399eadcb = $(`<div id="html_cb06267ad3b164f9c11b11a5399eadcb" style="width: 100.0%; height: 100.0%;"><b>Lake Placid</b><br>Population (approx): 2,350<br><i>Adirondack High Peaks (Keene/Keene Valley, Lake Placid)</i></div>`)[0];
            popup_288b50afd9b21105971c77f7796f23ba.setContent(html_cb06267ad3b164f9c11b11a5399eadcb);
        

        circle_marker_009c049a4e02003d7ba29c098de96be1.bindPopup(popup_288b50afd9b21105971c77f7796f23ba)
        ;

        
    
    
            circle_marker_009c049a4e02003d7ba29c098de96be1.bindTooltip(
                `<div>
                     Lake Placid (~2,350) - 5h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_0339f3db2825a25520ca154a95eb2427 = L.circleMarker(
                [44.33, -74.13],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 5.878775382679628, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_350521b1d8ac43429ec57e2f5ef1b0b9 = L.popup({"maxWidth": 260});

        
            var html_9050c41ccf5ab695a79b1899c7484d45 = $(`<div id="html_9050c41ccf5ab695a79b1899c7484d45" style="width: 100.0%; height: 100.0%;"><b>Saranac Lake</b><br>Population (approx): 5,400<br><i>Adirondack High Peaks (Keene/Keene Valley, Lake Placid)</i></div>`)[0];
            popup_350521b1d8ac43429ec57e2f5ef1b0b9.setContent(html_9050c41ccf5ab695a79b1899c7484d45);
        

        circle_marker_0339f3db2825a25520ca154a95eb2427.bindPopup(popup_350521b1d8ac43429ec57e2f5ef1b0b9)
        ;

        
    
    
            circle_marker_0339f3db2825a25520ca154a95eb2427.bindTooltip(
                `<div>
                     Saranac Lake (~5,400) - 5h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_602126efd9c0605e56a40fabea171eaf = L.circleMarker(
                [44.22, -74.46],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 4.595650117230423, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_8be3bad8d6eaf09c1badea42eb78cda2 = L.popup({"maxWidth": 260});

        
            var html_403399ccd60cd386e159e8a1173f3cc8 = $(`<div id="html_403399ccd60cd386e159e8a1173f3cc8" style="width: 100.0%; height: 100.0%;"><b>Tupper Lake</b><br>Population (approx): 3,300<br><i>Adirondack High Peaks (Keene/Keene Valley, Lake Placid)</i></div>`)[0];
            popup_8be3bad8d6eaf09c1badea42eb78cda2.setContent(html_403399ccd60cd386e159e8a1173f3cc8);
        

        circle_marker_602126efd9c0605e56a40fabea171eaf.bindPopup(popup_8be3bad8d6eaf09c1badea42eb78cda2)
        ;

        
    
    
            circle_marker_602126efd9c0605e56a40fabea171eaf.bindTooltip(
                `<div>
                     Tupper Lake (~3,300) - 5h 30m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_f8fe64dc588133db3dc954b49ae16461 = L.circleMarker(
                [44.29, -73.79],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_d869402937d5c62e01caf9b6efd5ca49 = L.popup({"maxWidth": 260});

        
            var html_6306fc9419551c5c14ead4b5839b2619 = $(`<div id="html_6306fc9419551c5c14ead4b5839b2619" style="width: 100.0%; height: 100.0%;"><b>Keene</b><br>Population (approx): 1,100<br><i>Adirondack High Peaks (Keene/Keene Valley, Lake Placid)</i></div>`)[0];
            popup_d869402937d5c62e01caf9b6efd5ca49.setContent(html_6306fc9419551c5c14ead4b5839b2619);
        

        circle_marker_f8fe64dc588133db3dc954b49ae16461.bindPopup(popup_d869402937d5c62e01caf9b6efd5ca49)
        ;

        
    
    
            circle_marker_f8fe64dc588133db3dc954b49ae16461.bindTooltip(
                `<div>
                     Keene (~1,100) - 4h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_55e9e0c0fe0c859e3ddbeaba02cb05a8 = L.circleMarker(
                [44.38, -73.87],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_5bb7356dad6ee855175538b2f48740d6 = L.popup({"maxWidth": 260});

        
            var html_da01ecbfa54a76687c6e7547a263113b = $(`<div id="html_da01ecbfa54a76687c6e7547a263113b" style="width: 100.0%; height: 100.0%;"><b>Wilmington</b><br>Population (approx): 1,250<br><i>Adirondack High Peaks (Keene/Keene Valley, Lake Placid)</i></div>`)[0];
            popup_5bb7356dad6ee855175538b2f48740d6.setContent(html_da01ecbfa54a76687c6e7547a263113b);
        

        circle_marker_55e9e0c0fe0c859e3ddbeaba02cb05a8.bindPopup(popup_5bb7356dad6ee855175538b2f48740d6)
        ;

        
    
    
            circle_marker_55e9e0c0fe0c859e3ddbeaba02cb05a8.bindTooltip(
                `<div>
                     Wilmington (~1,250) - 4h 30m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_4c2a3ae6017800d63fabdfcd145e5925 = L.circleMarker(
                [43.43, -73.71],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_4cd11d3faafdc0084967c2534735b666 = L.popup({"maxWidth": 260});

        
            var html_39a95bd33f8db867a039eb53839ba6af = $(`<div id="html_39a95bd33f8db867a039eb53839ba6af" style="width: 100.0%; height: 100.0%;"><b>Lake George</b><br>Population (approx): 1,000<br><i>Lake George & Pharaoh Lake Wilderness</i></div>`)[0];
            popup_4cd11d3faafdc0084967c2534735b666.setContent(html_39a95bd33f8db867a039eb53839ba6af);
        

        circle_marker_4c2a3ae6017800d63fabdfcd145e5925.bindPopup(popup_4cd11d3faafdc0084967c2534735b666)
        ;

        
    
    
            circle_marker_4c2a3ae6017800d63fabdfcd145e5925.bindTooltip(
                `<div>
                     Lake George (~1,000) - 3h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_ed31d8c825bd39c58ae1c770f65ed822 = L.circleMarker(
                [43.55, -73.65],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.752332607858744, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_0c68ddbe55312648f298e58611e499a7 = L.popup({"maxWidth": 260});

        
            var html_d43157f096256a3786a1194fb8b1d36f = $(`<div id="html_d43157f096256a3786a1194fb8b1d36f" style="width: 100.0%; height: 100.0%;"><b>Bolton</b><br>Population (approx): 2,200<br><i>Lake George & Pharaoh Lake Wilderness</i></div>`)[0];
            popup_0c68ddbe55312648f298e58611e499a7.setContent(html_d43157f096256a3786a1194fb8b1d36f);
        

        circle_marker_ed31d8c825bd39c58ae1c770f65ed822.bindPopup(popup_0c68ddbe55312648f298e58611e499a7)
        ;

        
    
    
            circle_marker_ed31d8c825bd39c58ae1c770f65ed822.bindTooltip(
                `<div>
                     Bolton (~2,200) - 3h 30m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_271634736d20260abf36c99fe0e70ecf = L.circleMarker(
                [43.84, -73.42],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 5.542562584220408, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_e453da595c06804e617b3091cfd9bcf7 = L.popup({"maxWidth": 260});

        
            var html_7d5cd034bcfedc435c09fc0b64ff143e = $(`<div id="html_7d5cd034bcfedc435c09fc0b64ff143e" style="width: 100.0%; height: 100.0%;"><b>Ticonderoga</b><br>Population (approx): 4,800<br><i>Lake George & Pharaoh Lake Wilderness</i></div>`)[0];
            popup_e453da595c06804e617b3091cfd9bcf7.setContent(html_7d5cd034bcfedc435c09fc0b64ff143e);
        

        circle_marker_271634736d20260abf36c99fe0e70ecf.bindPopup(popup_e453da595c06804e617b3091cfd9bcf7)
        ;

        
    
    
            circle_marker_271634736d20260abf36c99fe0e70ecf.bindTooltip(
                `<div>
                     Ticonderoga (~4,800) - 4h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_80e336fd7621320c1755a467d12f7654 = L.circleMarker(
                [42.21, -74.21],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.577708763999664, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_b204c0d64c9d236082ad61db8ccc66b0 = L.popup({"maxWidth": 260});

        
            var html_e0713a830dbac9014c5c306c4a48854b = $(`<div id="html_e0713a830dbac9014c5c306c4a48854b" style="width: 100.0%; height: 100.0%;"><b>Hunter</b><br>Population (approx): 2,000<br><i>Catskills (Slide, Hunter, Kaaterskill)</i></div>`)[0];
            popup_b204c0d64c9d236082ad61db8ccc66b0.setContent(html_e0713a830dbac9014c5c306c4a48854b);
        

        circle_marker_80e336fd7621320c1755a467d12f7654.bindPopup(popup_b204c0d64c9d236082ad61db8ccc66b0)
        ;

        
    
    
            circle_marker_80e336fd7621320c1755a467d12f7654.bindTooltip(
                `<div>
                     Hunter (~2,000) - 2h 30m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_79d3ceb65f8d1eecd55c35ec20feb11e = L.circleMarker(
                [42.19, -74.13],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_699c50d31a3c8c151884e050ae49f2dd = L.popup({"maxWidth": 260});

        
            var html_1da523ae099591667fed332dbc9a0ccc = $(`<div id="html_1da523ae099591667fed332dbc9a0ccc" style="width: 100.0%; height: 100.0%;"><b>Tannersville</b><br>Population (approx): 600<br><i>Catskills (Slide, Hunter, Kaaterskill)</i></div>`)[0];
            popup_699c50d31a3c8c151884e050ae49f2dd.setContent(html_1da523ae099591667fed332dbc9a0ccc);
        

        circle_marker_79d3ceb65f8d1eecd55c35ec20feb11e.bindPopup(popup_699c50d31a3c8c151884e050ae49f2dd)
        ;

        
    
    
            circle_marker_79d3ceb65f8d1eecd55c35ec20feb11e.bindTooltip(
                `<div>
                     Tannersville (~600) - 2h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_ca9ff7aff737cb1bda7f1d9028cd0bd6 = L.circleMarker(
                [42.04, -74.12],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 6.196773353931867, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_217c71322c4ebb2e9b79b84b18940d05 = L.popup({"maxWidth": 260});

        
            var html_97b8e13aa83a3160ee99994740759555 = $(`<div id="html_97b8e13aa83a3160ee99994740759555" style="width: 100.0%; height: 100.0%;"><b>Woodstock</b><br>Population (approx): 6,000<br><i>Catskills (Slide, Hunter, Kaaterskill)</i></div>`)[0];
            popup_217c71322c4ebb2e9b79b84b18940d05.setContent(html_97b8e13aa83a3160ee99994740759555);
        

        circle_marker_ca9ff7aff737cb1bda7f1d9028cd0bd6.bindPopup(popup_217c71322c4ebb2e9b79b84b18940d05)
        ;

        
    
    
            circle_marker_ca9ff7aff737cb1bda7f1d9028cd0bd6.bindTooltip(
                `<div>
                     Woodstock (~6,000) - 2h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_7437efc1dd3d70b18f9bc0a920bf88fd = L.circleMarker(
                [42.08, -74.31],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_6127e7729f4adf50892cde0521c15300 = L.popup({"maxWidth": 260});

        
            var html_a03e63a6390bdb1c5c6bc560e567fbd3 = $(`<div id="html_a03e63a6390bdb1c5c6bc560e567fbd3" style="width: 100.0%; height: 100.0%;"><b>Phoenicia</b><br>Population (approx): 300<br><i>Catskills (Slide, Hunter, Kaaterskill)</i></div>`)[0];
            popup_6127e7729f4adf50892cde0521c15300.setContent(html_a03e63a6390bdb1c5c6bc560e567fbd3);
        

        circle_marker_7437efc1dd3d70b18f9bc0a920bf88fd.bindPopup(popup_6127e7729f4adf50892cde0521c15300)
        ;

        
    
    
            circle_marker_7437efc1dd3d70b18f9bc0a920bf88fd.bindTooltip(
                `<div>
                     Phoenicia (~300) - 2h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_2f8f8b6d4c5d77eba799aebea5b33bf7 = L.circleMarker(
                [42.3, -74.26],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.2984845004941286, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_d4d4b0f512687238451d0e4679bc4e9c = L.popup({"maxWidth": 260});

        
            var html_2f64dd36fff5df04241aa08e50912909 = $(`<div id="html_2f64dd36fff5df04241aa08e50912909" style="width: 100.0%; height: 100.0%;"><b>Windham</b><br>Population (approx): 1,700<br><i>Catskills (Slide, Hunter, Kaaterskill)</i></div>`)[0];
            popup_d4d4b0f512687238451d0e4679bc4e9c.setContent(html_2f64dd36fff5df04241aa08e50912909);
        

        circle_marker_2f8f8b6d4c5d77eba799aebea5b33bf7.bindPopup(popup_d4d4b0f512687238451d0e4679bc4e9c)
        ;

        
    
    
            circle_marker_2f8f8b6d4c5d77eba799aebea5b33bf7.bindTooltip(
                `<div>
                     Windham (~1,700) - 2h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_d98de2147a59b3188db3a8838b445f45 = L.circleMarker(
                [41.75, -74.09],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 9.465727652959385, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_84cc434547cb0533de854833c46349c8 = L.popup({"maxWidth": 260});

        
            var html_cc4ac400dc1a6a1abeade60e4cb63fa3 = $(`<div id="html_cc4ac400dc1a6a1abeade60e4cb63fa3" style="width: 100.0%; height: 100.0%;"><b>New Paltz</b><br>Population (approx): 14,000<br><i>Shawangunks / Minnewaska & Mohonk Preserve</i></div>`)[0];
            popup_84cc434547cb0533de854833c46349c8.setContent(html_cc4ac400dc1a6a1abeade60e4cb63fa3);
        

        circle_marker_d98de2147a59b3188db3a8838b445f45.bindPopup(popup_84cc434547cb0533de854833c46349c8)
        ;

        
    
    
            circle_marker_d98de2147a59b3188db3a8838b445f45.bindTooltip(
                `<div>
                     New Paltz (~14,000) - 1h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_5073d321307b626d0170289d248862c4 = L.circleMarker(
                [41.68, -74.16],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 6.196773353931867, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_98ecb6a9f2d5e1244ca4a680df5efe20 = L.popup({"maxWidth": 260});

        
            var html_04d94cde6497dd0e50742fe6ab8118ae = $(`<div id="html_04d94cde6497dd0e50742fe6ab8118ae" style="width: 100.0%; height: 100.0%;"><b>Gardiner</b><br>Population (approx): 6,000<br><i>Shawangunks / Minnewaska & Mohonk Preserve</i></div>`)[0];
            popup_98ecb6a9f2d5e1244ca4a680df5efe20.setContent(html_04d94cde6497dd0e50742fe6ab8118ae);
        

        circle_marker_5073d321307b626d0170289d248862c4.bindPopup(popup_98ecb6a9f2d5e1244ca4a680df5efe20)
        ;

        
    
    
            circle_marker_5073d321307b626d0170289d248862c4.bindTooltip(
                `<div>
                     Gardiner (~6,000) - 1h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_150d95768cb03633699a11655b6c6529 = L.circleMarker(
                [41.84, -74.08],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 6.196773353931867, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_6cf0938623501b2846a741350166fda4 = L.popup({"maxWidth": 260});

        
            var html_46c23bfe3216c023e6f961efac7bbf6d = $(`<div id="html_46c23bfe3216c023e6f961efac7bbf6d" style="width: 100.0%; height: 100.0%;"><b>Rosendale</b><br>Population (approx): 6,000<br><i>Shawangunks / Minnewaska & Mohonk Preserve</i></div>`)[0];
            popup_6cf0938623501b2846a741350166fda4.setContent(html_46c23bfe3216c023e6f961efac7bbf6d);
        

        circle_marker_150d95768cb03633699a11655b6c6529.bindPopup(popup_6cf0938623501b2846a741350166fda4)
        ;

        
    
    
            circle_marker_150d95768cb03633699a11655b6c6529.bindTooltip(
                `<div>
                     Rosendale (~6,000) - 1h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_eed42e0fc2fc672ff4c49eb3c595d3bc = L.circleMarker(
                [41.72, -74.4],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 5.059644256269407, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_0fd892d74e7b337b85a4cbb0cb909efd = L.popup({"maxWidth": 260});

        
            var html_ca52cb6c38f71f7d3b100bcc6b498e26 = $(`<div id="html_ca52cb6c38f71f7d3b100bcc6b498e26" style="width: 100.0%; height: 100.0%;"><b>Ellenville</b><br>Population (approx): 4,000<br><i>Shawangunks / Minnewaska & Mohonk Preserve</i></div>`)[0];
            popup_0fd892d74e7b337b85a4cbb0cb909efd.setContent(html_ca52cb6c38f71f7d3b100bcc6b498e26);
        

        circle_marker_eed42e0fc2fc672ff4c49eb3c595d3bc.bindPopup(popup_0fd892d74e7b337b85a4cbb0cb909efd)
        ;

        
    
    
            circle_marker_eed42e0fc2fc672ff4c49eb3c595d3bc.bindTooltip(
                `<div>
                     Ellenville (~4,000) - 2h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_db1a12d1794846d99284563278f958e3 = L.circleMarker(
                [41.5, -73.96],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 9.465727652959385, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_4c6726095cf497f4db6447be33db5024 = L.popup({"maxWidth": 260});

        
            var html_9d4aca6fb0ad0ed8efbef5dca24b6276 = $(`<div id="html_9d4aca6fb0ad0ed8efbef5dca24b6276" style="width: 100.0%; height: 100.0%;"><b>Beacon</b><br>Population (approx): 14,000<br><i>Hudson Highlands (Breakneck, Storm King, Bull Hill)</i></div>`)[0];
            popup_4c6726095cf497f4db6447be33db5024.setContent(html_9d4aca6fb0ad0ed8efbef5dca24b6276);
        

        circle_marker_db1a12d1794846d99284563278f958e3.bindPopup(popup_4c6726095cf497f4db6447be33db5024)
        ;

        
    
    
            circle_marker_db1a12d1794846d99284563278f958e3.bindTooltip(
                `<div>
                     Beacon (~14,000) - 1h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_de6c206b4502db4b373b8f80340a3eb3 = L.circleMarker(
                [41.42, -73.95],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.577708763999664, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_e7b5f82c57cde5123c5462cf12c45316 = L.popup({"maxWidth": 260});

        
            var html_124ca7db2a0454ec6d9dd0a73545b961 = $(`<div id="html_124ca7db2a0454ec6d9dd0a73545b961" style="width: 100.0%; height: 100.0%;"><b>Cold Spring</b><br>Population (approx): 2,000<br><i>Hudson Highlands (Breakneck, Storm King, Bull Hill)</i></div>`)[0];
            popup_e7b5f82c57cde5123c5462cf12c45316.setContent(html_124ca7db2a0454ec6d9dd0a73545b961);
        

        circle_marker_de6c206b4502db4b373b8f80340a3eb3.bindPopup(popup_e7b5f82c57cde5123c5462cf12c45316)
        ;

        
    
    
            circle_marker_de6c206b4502db4b373b8f80340a3eb3.bindTooltip(
                `<div>
                     Cold Spring (~2,000) - 1h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_cdf71865d5fde1bf57e59eb3f37a1d06 = L.circleMarker(
                [41.44, -74.02],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 4.3817804600413295, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_cabbdbcaf9b97ebe8015a53eefcbcacd = L.popup({"maxWidth": 260});

        
            var html_f33dbe4858ae335155ea39e60ffadb4a = $(`<div id="html_f33dbe4858ae335155ea39e60ffadb4a" style="width: 100.0%; height: 100.0%;"><b>Cornwall-on-Hudson</b><br>Population (approx): 3,000<br><i>Hudson Highlands (Breakneck, Storm King, Bull Hill)</i></div>`)[0];
            popup_cabbdbcaf9b97ebe8015a53eefcbcacd.setContent(html_f33dbe4858ae335155ea39e60ffadb4a);
        

        circle_marker_cdf71865d5fde1bf57e59eb3f37a1d06.bindPopup(popup_cabbdbcaf9b97ebe8015a53eefcbcacd)
        ;

        
    
    
            circle_marker_cdf71865d5fde1bf57e59eb3f37a1d06.bindTooltip(
                `<div>
                     Cornwall-on-Hudson (~3,000) - 1h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_4ef79c552251e02f8814e4db40845c91 = L.circleMarker(
                [41.5, -74.01],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 13.386560424545209, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_06c72aa9e6dc67417a6e2c69dbed2083 = L.popup({"maxWidth": 260});

        
            var html_7d6cfaeaef59d008422ab6b944aca6b1 = $(`<div id="html_7d6cfaeaef59d008422ab6b944aca6b1" style="width: 100.0%; height: 100.0%;"><b>Newburgh</b><br>Population (approx): 28,000<br><i>Hudson Highlands (Breakneck, Storm King, Bull Hill)</i></div>`)[0];
            popup_06c72aa9e6dc67417a6e2c69dbed2083.setContent(html_7d6cfaeaef59d008422ab6b944aca6b1);
        

        circle_marker_4ef79c552251e02f8814e4db40845c91.bindPopup(popup_06c72aa9e6dc67417a6e2c69dbed2083)
        ;

        
    
    
            circle_marker_4ef79c552251e02f8814e4db40845c91.bindTooltip(
                `<div>
                     Newburgh (~28,000) - 1h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_ffb7bb97ef74c18528da349ae672b8e3 = L.circleMarker(
                [41.31, -74.14],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 4.079215610874228, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_1f8b0c6228093438a0fdb5e5c8747f13 = L.popup({"maxWidth": 260});

        
            var html_7e54cee3d3d00ba1d1789d8b02a18c1e = $(`<div id="html_7e54cee3d3d00ba1d1789d8b02a18c1e" style="width: 100.0%; height: 100.0%;"><b>Harriman</b><br>Population (approx): 2,600<br><i>Harriman–Bear Mountain State Parks</i></div>`)[0];
            popup_1f8b0c6228093438a0fdb5e5c8747f13.setContent(html_7e54cee3d3d00ba1d1789d8b02a18c1e);
        

        circle_marker_ffb7bb97ef74c18528da349ae672b8e3.bindPopup(popup_1f8b0c6228093438a0fdb5e5c8747f13)
        ;

        
    
    
            circle_marker_ffb7bb97ef74c18528da349ae672b8e3.bindTooltip(
                `<div>
                     Harriman (~2,600) - 1h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_5712225a3dbd22275e5fc9052633dbef = L.circleMarker(
                [41.16, -74.19],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 4.454211490264018, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_5bea9b82dd9485d31f1aff10aa1ee5b8 = L.popup({"maxWidth": 260});

        
            var html_67bebfc53637d05fdd706058e82519e1 = $(`<div id="html_67bebfc53637d05fdd706058e82519e1" style="width: 100.0%; height: 100.0%;"><b>Sloatsburg</b><br>Population (approx): 3,100<br><i>Harriman–Bear Mountain State Parks</i></div>`)[0];
            popup_5bea9b82dd9485d31f1aff10aa1ee5b8.setContent(html_67bebfc53637d05fdd706058e82519e1);
        

        circle_marker_5712225a3dbd22275e5fc9052633dbef.bindPopup(popup_5bea9b82dd9485d31f1aff10aa1ee5b8)
        ;

        
    
    
            circle_marker_5712225a3dbd22275e5fc9052633dbef.bindTooltip(
                `<div>
                     Sloatsburg (~3,100) - 1h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_1376d641a66fcdf6870af5d823d2cc2d = L.circleMarker(
                [41.33, -74.18],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 11.027239001672179, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_a2973c755dce96ddfa8d2c1479fd831a = L.popup({"maxWidth": 260});

        
            var html_2928e105c3b7bcf6c123b30df17b9729 = $(`<div id="html_2928e105c3b7bcf6c123b30df17b9729" style="width: 100.0%; height: 100.0%;"><b>Monroe</b><br>Population (approx): 19,000<br><i>Harriman–Bear Mountain State Parks</i></div>`)[0];
            popup_a2973c755dce96ddfa8d2c1479fd831a.setContent(html_2928e105c3b7bcf6c123b30df17b9729);
        

        circle_marker_1376d641a66fcdf6870af5d823d2cc2d.bindPopup(popup_a2973c755dce96ddfa8d2c1479fd831a)
        ;

        
    
    
            circle_marker_1376d641a66fcdf6870af5d823d2cc2d.bindTooltip(
                `<div>
                     Monroe (~19,000) - 1h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_cdf339bf802e9da8952d41255e62bd57 = L.circleMarker(
                [41.23, -73.99],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 9.797958971132713, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_915c0b4f016fb59fefa055d41a41ff2e = L.popup({"maxWidth": 260});

        
            var html_378ebd8a91ac110ae43551d6a88a299f = $(`<div id="html_378ebd8a91ac110ae43551d6a88a299f" style="width: 100.0%; height: 100.0%;"><b>Stony Point</b><br>Population (approx): 15,000<br><i>Harriman–Bear Mountain State Parks</i></div>`)[0];
            popup_915c0b4f016fb59fefa055d41a41ff2e.setContent(html_378ebd8a91ac110ae43551d6a88a299f);
        

        circle_marker_cdf339bf802e9da8952d41255e62bd57.bindPopup(popup_915c0b4f016fb59fefa055d41a41ff2e)
        ;

        
    
    
            circle_marker_cdf339bf802e9da8952d41255e62bd57.bindTooltip(
                `<div>
                     Stony Point (~15,000) - 1h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_850e0862ca9a0178616fa813596bacc2 = L.circleMarker(
                [41.33, -73.99],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_3c95751c97b39ef24316f07ce40649a1 = L.popup({"maxWidth": 260});

        
            var html_3c0b0f7e8f8d8d9f470cc595903d685f = $(`<div id="html_3c0b0f7e8f8d8d9f470cc595903d685f" style="width: 100.0%; height: 100.0%;"><b>Fort Montgomery</b><br>Population (approx): 1,400<br><i>Harriman–Bear Mountain State Parks</i></div>`)[0];
            popup_3c95751c97b39ef24316f07ce40649a1.setContent(html_3c0b0f7e8f8d8d9f470cc595903d685f);
        

        circle_marker_850e0862ca9a0178616fa813596bacc2.bindPopup(popup_3c95751c97b39ef24316f07ce40649a1)
        ;

        
    
    
            circle_marker_850e0862ca9a0178616fa813596bacc2.bindTooltip(
                `<div>
                     Fort Montgomery (~1,400) - 1h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_d45a72ea9ad670d636e21f6b569c0628 = L.circleMarker(
                [42.44, -76.5],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 14.310835055998655, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_22558b813e2a38bd45589d5de819cc4e = L.popup({"maxWidth": 260});

        
            var html_8dbedb4358a15931cc7cff2e32447717 = $(`<div id="html_8dbedb4358a15931cc7cff2e32447717" style="width: 100.0%; height: 100.0%;"><b>Ithaca</b><br>Population (approx): 32,000<br><i>Finger Lakes Gorges (Ithaca area)</i></div>`)[0];
            popup_22558b813e2a38bd45589d5de819cc4e.setContent(html_8dbedb4358a15931cc7cff2e32447717);
        

        circle_marker_d45a72ea9ad670d636e21f6b569c0628.bindPopup(popup_22558b813e2a38bd45589d5de819cc4e)
        ;

        
    
    
            circle_marker_d45a72ea9ad670d636e21f6b569c0628.bindTooltip(
                `<div>
                     Ithaca (~32,000) - 4h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_3b8391386008fd5ec745248e26a60729 = L.circleMarker(
                [42.49, -76.3],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 9.465727652959385, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_f0a243e6c3731d5779d8f1cd65f35ac9 = L.popup({"maxWidth": 260});

        
            var html_c7134758fe326a08d245625dfaf8ead1 = $(`<div id="html_c7134758fe326a08d245625dfaf8ead1" style="width: 100.0%; height: 100.0%;"><b>Dryden</b><br>Population (approx): 14,000<br><i>Finger Lakes Gorges (Ithaca area)</i></div>`)[0];
            popup_f0a243e6c3731d5779d8f1cd65f35ac9.setContent(html_c7134758fe326a08d245625dfaf8ead1);
        

        circle_marker_3b8391386008fd5ec745248e26a60729.bindPopup(popup_f0a243e6c3731d5779d8f1cd65f35ac9)
        ;

        
    
    
            circle_marker_3b8391386008fd5ec745248e26a60729.bindTooltip(
                `<div>
                     Dryden (~14,000) - 4h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_e8f89dd3a0c99b73a45e5f2bf5f5dd6e = L.circleMarker(
                [42.54, -76.66],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.3941125496954285, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_3d8050d00ca35bc16d11db8ec00b7511 = L.popup({"maxWidth": 260});

        
            var html_10440a14774f3c9ed287eb493c61bebd = $(`<div id="html_10440a14774f3c9ed287eb493c61bebd" style="width: 100.0%; height: 100.0%;"><b>Trumansburg</b><br>Population (approx): 1,800<br><i>Finger Lakes Gorges (Ithaca area)</i></div>`)[0];
            popup_3d8050d00ca35bc16d11db8ec00b7511.setContent(html_10440a14774f3c9ed287eb493c61bebd);
        

        circle_marker_e8f89dd3a0c99b73a45e5f2bf5f5dd6e.bindPopup(popup_3d8050d00ca35bc16d11db8ec00b7511)
        ;

        
    
    
            circle_marker_e8f89dd3a0c99b73a45e5f2bf5f5dd6e.bindTooltip(
                `<div>
                     Trumansburg (~1,800) - 4h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_7901083d82da032ff03a72cb063a6667 = L.circleMarker(
                [42.38, -76.87],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.3941125496954285, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_bf0b9b12953834c612ddb47bfc9b41d2 = L.popup({"maxWidth": 260});

        
            var html_b3020bac16931ac14dd1c19139779814 = $(`<div id="html_b3020bac16931ac14dd1c19139779814" style="width: 100.0%; height: 100.0%;"><b>Watkins Glen</b><br>Population (approx): 1,800<br><i>Watkins Glen & Surrounds</i></div>`)[0];
            popup_bf0b9b12953834c612ddb47bfc9b41d2.setContent(html_b3020bac16931ac14dd1c19139779814);
        

        circle_marker_7901083d82da032ff03a72cb063a6667.bindPopup(popup_bf0b9b12953834c612ddb47bfc9b41d2)
        ;

        
    
    
            circle_marker_7901083d82da032ff03a72cb063a6667.bindTooltip(
                `<div>
                     Watkins Glen (~1,800) - 4h 30m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_b897172f92c5f96a561c87c914dc60e7 = L.circleMarker(
                [42.35, -76.85],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.2, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_6efa71cc8bf6e2798bc744addb90ae1d = L.popup({"maxWidth": 260});

        
            var html_3e56416a801234267857f9ed8ff8af3f = $(`<div id="html_3e56416a801234267857f9ed8ff8af3f" style="width: 100.0%; height: 100.0%;"><b>Montour Falls</b><br>Population (approx): 1,600<br><i>Watkins Glen & Surrounds</i></div>`)[0];
            popup_6efa71cc8bf6e2798bc744addb90ae1d.setContent(html_3e56416a801234267857f9ed8ff8af3f);
        

        circle_marker_b897172f92c5f96a561c87c914dc60e7.bindPopup(popup_6efa71cc8bf6e2798bc744addb90ae1d)
        ;

        
    
    
            circle_marker_b897172f92c5f96a561c87c914dc60e7.bindTooltip(
                `<div>
                     Montour Falls (~1,600) - 4h 30m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_3d266afd36de2c87540981ce5c053d51 = L.circleMarker(
                [42.33, -76.79],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_17f08fd19dfde9abb51c8bf681d06226 = L.popup({"maxWidth": 260});

        
            var html_ceff98b433a26cfc1280ecccf67fe111 = $(`<div id="html_ceff98b433a26cfc1280ecccf67fe111" style="width: 100.0%; height: 100.0%;"><b>Odessa</b><br>Population (approx): 600<br><i>Watkins Glen & Surrounds</i></div>`)[0];
            popup_17f08fd19dfde9abb51c8bf681d06226.setContent(html_ceff98b433a26cfc1280ecccf67fe111);
        

        circle_marker_3d266afd36de2c87540981ce5c053d51.bindPopup(popup_17f08fd19dfde9abb51c8bf681d06226)
        ;

        
    
    
            circle_marker_3d266afd36de2c87540981ce5c053d51.bindTooltip(
                `<div>
                     Odessa (~600) - 4h 30m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_14d56bfc353f38c5cc8702607c41f21c = L.circleMarker(
                [42.73, -77.88],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 5.2459508194416005, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_8026508e5a65fa2aa87291756c654244 = L.popup({"maxWidth": 260});

        
            var html_f7bcdcd7deca4cfa4574aba911d99b95 = $(`<div id="html_f7bcdcd7deca4cfa4574aba911d99b95" style="width: 100.0%; height: 100.0%;"><b>Mount Morris</b><br>Population (approx): 4,300<br><i>Letchworth State Park (Genesee River Gorge)</i></div>`)[0];
            popup_8026508e5a65fa2aa87291756c654244.setContent(html_f7bcdcd7deca4cfa4574aba911d99b95);
        

        circle_marker_14d56bfc353f38c5cc8702607c41f21c.bindPopup(popup_8026508e5a65fa2aa87291756c654244)
        ;

        
    
    
            circle_marker_14d56bfc353f38c5cc8702607c41f21c.bindTooltip(
                `<div>
                     Mount Morris (~4,300) - 6h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_459845d1cfdbb6d1ba2e55b2eb322f45 = L.circleMarker(
                [42.72, -78.0],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 4.8, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_c3b86257b11de79d1cd3cc7f3834fdc0 = L.popup({"maxWidth": 260});

        
            var html_443552a270f3738016274b3b20dd7b3b = $(`<div id="html_443552a270f3738016274b3b20dd7b3b" style="width: 100.0%; height: 100.0%;"><b>Perry</b><br>Population (approx): 3,600<br><i>Letchworth State Park (Genesee River Gorge)</i></div>`)[0];
            popup_c3b86257b11de79d1cd3cc7f3834fdc0.setContent(html_443552a270f3738016274b3b20dd7b3b);
        

        circle_marker_459845d1cfdbb6d1ba2e55b2eb322f45.bindPopup(popup_c3b86257b11de79d1cd3cc7f3834fdc0)
        ;

        
    
    
            circle_marker_459845d1cfdbb6d1ba2e55b2eb322f45.bindTooltip(
                `<div>
                     Perry (~3,600) - 6h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_3dae15daa6ed32944c2e89715f6633a5 = L.circleMarker(
                [42.63, -78.05],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 4.233202097703345, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_9d4a20374337b69ed7976bde91961aaa = L.popup({"maxWidth": 260});

        
            var html_0b7b2ba94651a3f8fdd473194eede930 = $(`<div id="html_0b7b2ba94651a3f8fdd473194eede930" style="width: 100.0%; height: 100.0%;"><b>Castile</b><br>Population (approx): 2,800<br><i>Letchworth State Park (Genesee River Gorge)</i></div>`)[0];
            popup_9d4a20374337b69ed7976bde91961aaa.setContent(html_0b7b2ba94651a3f8fdd473194eede930);
        

        circle_marker_3dae15daa6ed32944c2e89715f6633a5.bindPopup(popup_9d4a20374337b69ed7976bde91961aaa)
        ;

        
    
    
            circle_marker_3dae15daa6ed32944c2e89715f6633a5.bindTooltip(
                `<div>
                     Castile (~2,800) - 6h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_75dffa3c8e33004f4b65f7399a4c396f = L.circleMarker(
                [42.16, -78.74],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 6.144916598294887, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_c8eeb41c778645f221fe123bef91634a = L.popup({"maxWidth": 260});

        
            var html_8331c74bbbfa28ce75816b66994e5d75 = $(`<div id="html_8331c74bbbfa28ce75816b66994e5d75" style="width: 100.0%; height: 100.0%;"><b>Salamanca</b><br>Population (approx): 5,900<br><i>Allegany State Park (Southern Tier)</i></div>`)[0];
            popup_c8eeb41c778645f221fe123bef91634a.setContent(html_8331c74bbbfa28ce75816b66994e5d75);
        

        circle_marker_75dffa3c8e33004f4b65f7399a4c396f.bindPopup(popup_c8eeb41c778645f221fe123bef91634a)
        ;

        
    
    
            circle_marker_75dffa3c8e33004f4b65f7399a4c396f.bindTooltip(
                `<div>
                     Salamanca (~5,900) - 7h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_3b0cd0e216d169c011b5c8b31c8b085a = L.circleMarker(
                [42.02, -78.63],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_4a1ab0841d15d71902da74ab6b37535f = L.popup({"maxWidth": 260});

        
            var html_00fae211e44cc896ee9c2ef259a06b9e = $(`<div id="html_00fae211e44cc896ee9c2ef259a06b9e" style="width: 100.0%; height: 100.0%;"><b>Limestone</b><br>Population (approx): 1,000<br><i>Allegany State Park (Southern Tier)</i></div>`)[0];
            popup_4a1ab0841d15d71902da74ab6b37535f.setContent(html_00fae211e44cc896ee9c2ef259a06b9e);
        

        circle_marker_3b0cd0e216d169c011b5c8b31c8b085a.bindPopup(popup_4a1ab0841d15d71902da74ab6b37535f)
        ;

        
    
    
            circle_marker_3b0cd0e216d169c011b5c8b31c8b085a.bindTooltip(
                `<div>
                     Limestone (~1,000) - 7h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_7fe429b4104adca0b8b98f2dd4471fa2 = L.circleMarker(
                [42.2, -78.65],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.577708763999664, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_79a2f88acaaafd0949bddd16b110e8f8 = L.popup({"maxWidth": 260});

        
            var html_10aec770e87ef79816ccb129c8e300e9 = $(`<div id="html_10aec770e87ef79816ccb129c8e300e9" style="width: 100.0%; height: 100.0%;"><b>Great Valley</b><br>Population (approx): 2,000<br><i>Allegany State Park (Southern Tier)</i></div>`)[0];
            popup_79a2f88acaaafd0949bddd16b110e8f8.setContent(html_10aec770e87ef79816ccb129c8e300e9);
        

        circle_marker_7fe429b4104adca0b8b98f2dd4471fa2.bindPopup(popup_79a2f88acaaafd0949bddd16b110e8f8)
        ;

        
    
    
            circle_marker_7fe429b4104adca0b8b98f2dd4471fa2.bindTooltip(
                `<div>
                     Great Valley (~2,000) - 7h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_50d1b49587e6a4609393bb2dc1e9d90a = L.circleMarker(
                [43.1, -79.03],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 17.527121840165318, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_9954770117e4601a3291e6d33b5daa4f = L.popup({"maxWidth": 260});

        
            var html_8c4e7c043913d026c8ae01c0a7763b04 = $(`<div id="html_8c4e7c043913d026c8ae01c0a7763b04" style="width: 100.0%; height: 100.0%;"><b>Niagara Falls (NY)</b><br>Population (approx): 48,000<br><i>Niagara Gorge (NY side)</i></div>`)[0];
            popup_9954770117e4601a3291e6d33b5daa4f.setContent(html_8c4e7c043913d026c8ae01c0a7763b04);
        

        circle_marker_50d1b49587e6a4609393bb2dc1e9d90a.bindPopup(popup_9954770117e4601a3291e6d33b5daa4f)
        ;

        
    
    
            circle_marker_50d1b49587e6a4609393bb2dc1e9d90a.bindTooltip(
                `<div>
                     Niagara Falls (NY) (~48,000) - 6h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_84db0f34a384c83f0d68ba875d27bbab = L.circleMarker(
                [43.17, -79.05],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 4.079215610874228, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_409cf6d007839dce4bc8914e45bf229b = L.popup({"maxWidth": 260});

        
            var html_992e416282e661855c3b7d9e7496a20e = $(`<div id="html_992e416282e661855c3b7d9e7496a20e" style="width: 100.0%; height: 100.0%;"><b>Lewiston</b><br>Population (approx): 2,600<br><i>Niagara Gorge (NY side)</i></div>`)[0];
            popup_409cf6d007839dce4bc8914e45bf229b.setContent(html_992e416282e661855c3b7d9e7496a20e);
        

        circle_marker_84db0f34a384c83f0d68ba875d27bbab.bindPopup(popup_409cf6d007839dce4bc8914e45bf229b)
        ;

        
    
    
            circle_marker_84db0f34a384c83f0d68ba875d27bbab.bindTooltip(
                `<div>
                     Lewiston (~2,600) - 6h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_ddd335f51a77cfd8634bd43d6028c9cb = L.circleMarker(
                [41.95, -73.51],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_a037480351ffee3f599e75f51bd3a587 = L.popup({"maxWidth": 260});

        
            var html_accb3620a75eddf4e4b60db2c8061e35 = $(`<div id="html_accb3620a75eddf4e4b60db2c8061e35" style="width: 100.0%; height: 100.0%;"><b>Millerton</b><br>Population (approx): 1,000<br><i>Taconic Range / Harlem Valley (incl. Bash Bish area)</i></div>`)[0];
            popup_a037480351ffee3f599e75f51bd3a587.setContent(html_accb3620a75eddf4e4b60db2c8061e35);
        

        circle_marker_ddd335f51a77cfd8634bd43d6028c9cb.bindPopup(popup_a037480351ffee3f599e75f51bd3a587)
        ;

        
    
    
            circle_marker_ddd335f51a77cfd8634bd43d6028c9cb.bindTooltip(
                `<div>
                     Millerton (~1,000) - 2h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_b452cdc5d9557d6c5665f9855308c91a = L.circleMarker(
                [41.84, -73.56],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 5.059644256269407, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_803a3e4ecc5afd8c5d7a9b045d632236 = L.popup({"maxWidth": 260});

        
            var html_9fc6be32f3bc89d23d35b6ffc14728c5 = $(`<div id="html_9fc6be32f3bc89d23d35b6ffc14728c5" style="width: 100.0%; height: 100.0%;"><b>Amenia</b><br>Population (approx): 4,000<br><i>Taconic Range / Harlem Valley (incl. Bash Bish area)</i></div>`)[0];
            popup_803a3e4ecc5afd8c5d7a9b045d632236.setContent(html_9fc6be32f3bc89d23d35b6ffc14728c5);
        

        circle_marker_b452cdc5d9557d6c5665f9855308c91a.bindPopup(popup_803a3e4ecc5afd8c5d7a9b045d632236)
        ;

        
    
    
            circle_marker_b452cdc5d9557d6c5665f9855308c91a.bindTooltip(
                `<div>
                     Amenia (~4,000) - 2h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_a48010c14b540265c6d67c68846b3f97 = L.circleMarker(
                [42.18, -73.53],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3.487119154832539, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_ef9e39d9f9fca98e996f66ec142a7609 = L.popup({"maxWidth": 260});

        
            var html_6603a17007ccb2691146351a38a9d354 = $(`<div id="html_6603a17007ccb2691146351a38a9d354" style="width: 100.0%; height: 100.0%;"><b>Hillsdale</b><br>Population (approx): 1,900<br><i>Taconic Range / Harlem Valley (incl. Bash Bish area)</i></div>`)[0];
            popup_ef9e39d9f9fca98e996f66ec142a7609.setContent(html_6603a17007ccb2691146351a38a9d354);
        

        circle_marker_a48010c14b540265c6d67c68846b3f97.bindPopup(popup_ef9e39d9f9fca98e996f66ec142a7609)
        ;

        
    
    
            circle_marker_a48010c14b540265c6d67c68846b3f97.bindTooltip(
                `<div>
                     Hillsdale (~1,900) - 2h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_3e12c483e1801ad384bad024916829f4 = L.circleMarker(
                [42.1, -73.57],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 4.595650117230423, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_7c118671e36c6d5041cca1b51bb59b0c = L.popup({"maxWidth": 260});

        
            var html_2ffe7f6b46a3d93b9bb864a1c89540fd = $(`<div id="html_2ffe7f6b46a3d93b9bb864a1c89540fd" style="width: 100.0%; height: 100.0%;"><b>Copake</b><br>Population (approx): 3,300<br><i>Taconic Range / Harlem Valley (incl. Bash Bish area)</i></div>`)[0];
            popup_7c118671e36c6d5041cca1b51bb59b0c.setContent(html_2ffe7f6b46a3d93b9bb864a1c89540fd);
        

        circle_marker_3e12c483e1801ad384bad024916829f4.bindPopup(popup_7c118671e36c6d5041cca1b51bb59b0c)
        ;

        
    
    
            circle_marker_3e12c483e1801ad384bad024916829f4.bindTooltip(
                `<div>
                     Copake (~3,300) - 2h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_e73258948ca9f579349120dd3bca5602 = L.circleMarker(
                [41.04, -71.94],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 5.059644256269407, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_3332b0a10338dcc6c4143b1441cc7075 = L.popup({"maxWidth": 260});

        
            var html_ac2242059f2ea8365dc37cd684d963b1 = $(`<div id="html_ac2242059f2ea8365dc37cd684d963b1" style="width: 100.0%; height: 100.0%;"><b>Montauk</b><br>Population (approx): 4,000<br><i>Long Island North & South Fork highlights (Montauk bluffs)</i></div>`)[0];
            popup_3332b0a10338dcc6c4143b1441cc7075.setContent(html_ac2242059f2ea8365dc37cd684d963b1);
        

        circle_marker_e73258948ca9f579349120dd3bca5602.bindPopup(popup_3332b0a10338dcc6c4143b1441cc7075)
        ;

        
    
    
            circle_marker_e73258948ca9f579349120dd3bca5602.bindTooltip(
                `<div>
                     Montauk (~4,000) - 3h 00m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_2c94504d7e27d3fb866180c0211ea3b6 = L.circleMarker(
                [40.98, -72.14],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 3, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_77a21fa64356f7ae16d1f1ff6b34583c = L.popup({"maxWidth": 260});

        
            var html_cc1f62d146a3e68adf3f4c2c39c10da6 = $(`<div id="html_cc1f62d146a3e68adf3f4c2c39c10da6" style="width: 100.0%; height: 100.0%;"><b>Amagansett</b><br>Population (approx): 1,100<br><i>Long Island North & South Fork highlights (Montauk bluffs)</i></div>`)[0];
            popup_77a21fa64356f7ae16d1f1ff6b34583c.setContent(html_cc1f62d146a3e68adf3f4c2c39c10da6);
        

        circle_marker_2c94504d7e27d3fb866180c0211ea3b6.bindPopup(popup_77a21fa64356f7ae16d1f1ff6b34583c)
        ;

        
    
    
            circle_marker_2c94504d7e27d3fb866180c0211ea3b6.bindTooltip(
                `<div>
                     Amagansett (~1,100) - 2h 45m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_d6dde1b99c8a8ae2a09a667e6547c2b9 = L.circleMarker(
                [40.9, -73.46],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 4.931531202375181, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_554c0b25f20271d4c52edc12d1cc19c4 = L.popup({"maxWidth": 260});

        
            var html_448920b31025fb40c3f6095782da8eeb = $(`<div id="html_448920b31025fb40c3f6095782da8eeb" style="width: 100.0%; height: 100.0%;"><b>Lloyd Harbor</b><br>Population (approx): 3,800<br><i>Caumsett State Historic Park Preserve (Lloyd Neck)</i></div>`)[0];
            popup_554c0b25f20271d4c52edc12d1cc19c4.setContent(html_448920b31025fb40c3f6095782da8eeb);
        

        circle_marker_d6dde1b99c8a8ae2a09a667e6547c2b9.bindPopup(popup_554c0b25f20271d4c52edc12d1cc19c4)
        ;

        
    
    
            circle_marker_d6dde1b99c8a8ae2a09a667e6547c2b9.bindTooltip(
                `<div>
                     Lloyd Harbor (~3,800) - 1h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var circle_marker_d97574657ac1d3424d9527a64dfb5a03 = L.circleMarker(
                [40.87, -73.45],
                {"bubblingMouseEvents": true, "color": "#000000", "dashArray": null, "dashOffset": null, "fill": true, "fillColor": "#000000", "fillOpacity": 0.7, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "opacity": 1.0, "radius": 5.656854249492381, "stroke": true, "weight": 1}
            ).addTo(feature_group_dacbddd05370aa53667cdcd0d78eedbe);
        
    
        var popup_1d15838cfcaa67fd08b2885e83e90239 = L.popup({"maxWidth": 260});

        
            var html_cc51fab29cd0cde995f856c429c52d1f = $(`<div id="html_cc51fab29cd0cde995f856c429c52d1f" style="width: 100.0%; height: 100.0%;"><b>Cold Spring Harbor</b><br>Population (approx): 5,000<br><i>Caumsett State Historic Park Preserve (Lloyd Neck)</i></div>`)[0];
            popup_1d15838cfcaa67fd08b2885e83e90239.setContent(html_cc51fab29cd0cde995f856c429c52d1f);
        

        circle_marker_d97574657ac1d3424d9527a64dfb5a03.bindPopup(popup_1d15838cfcaa67fd08b2885e83e90239)
        ;

        
    
    
            circle_marker_d97574657ac1d3424d9527a64dfb5a03.bindTooltip(
                `<div>
                     Cold Spring Harbor (~5,000) - 1h 15m
                 </div>`,
                {"sticky": true}
            );
        
    
            var layer_control_0bb602bf6d00bd1253fb54767d726586 = {
                base_layers : {
                    "cartodbpositron" : tile_layer_04c0d540e422a0223c0c65ed3a113aae,
                },
                overlays :  {
                    "Highlighted Regions (Polygons)" : feature_group_3983efa59c3fa7675054fceade5a1d6a,
                    "Top Spots (centroids)" : feature_group_045a5715d02866a8d3ae3f29fb7b4703,
                    "Population centers (scaled black dots)" : feature_group_dacbddd05370aa53667cdcd0d78eedbe,
                },
            };
            L.control.layers(
                layer_control_0bb602bf6d00bd1253fb54767d726586.base_layers,
                layer_control_0bb602bf6d00bd1253fb54767d726586.overlays,
                {"autoZIndex": true, "collapsed": false, "position": "topright"}
            ).addTo(map_9eb96eb1fe9bc3ea56b51a20c1cf6a00);
        
</script>
