from LastFM import *
from TheAudioDB import *
from TheMovieDB import *
from Utils import *
from local_db import *
from YouTube import *
from Trakt import *


def StartInfoActions(infos, params):
    if "artistname" in params:
        params["artistname"] = params.get("artistname", "").split(" feat. ")[0].strip()
        params["artist_mbid"] = fetch_musicbrainz_id(params["artistname"])
    prettyprint(params)
    prettyprint(infos)
    if "prefix" in params and (not params["prefix"].endswith('.')) and (params["prefix"] is not ""):
        params["prefix"] = params["prefix"] + '.'
    for info in infos:
        data = []
        #  Images
        if info == 'xkcd':
            from MiscScraper import GetXKCDInfo
            data = GetXKCDInfo(), "XKCD"
        elif info == 'cyanide':
            from MiscScraper import GetCandHInfo
            data = GetCandHInfo(), "CyanideHappiness"
        elif info == 'dailybabes':
            from MiscScraper import GetDailyBabes
            data = GetDailyBabes(), "DailyBabes"
        elif info == 'dailybabe':
            from MiscScraper import GetDailyBabes
            data = GetDailyBabes(single=True), "DailyBabe"
        # Audio
        elif info == 'discography':
            Discography = GetDiscography(params["artistname"])
            if not Discography:
                Discography = GetArtistTopAlbums(params.get("artist_mbid"))
            data = Discography, "Discography"
        elif info == 'mostlovedtracks':
            data = GetMostLovedTracks(params["artistname"]), "MostLovedTracks"
        elif info == 'artistdetails':
            ArtistDetails = GetArtistDetails(params["artistname"])
            passDictToSkin(ArtistDetails, params.get("prefix", ""))
            if "audiodbid" in ArtistDetails:
                data = GetMusicVideos(ArtistDetails["audiodbid"]), "MusicVideos"
        elif info == 'musicvideos':
            pass
            # if "audiodbid" in ArtistDetails:
            #     data = GetMusicVideos(ArtistDetails["audiodbid"]), "MusicVideos"
        elif info == 'albuminfo':
            if params.get("id", ""):
                AlbumDetails = GetAlbumDetails(params.get("id", ""))
                passDictToSkin(AlbumDetails, params.get("prefix", ""))
        elif info == 'trackdetails':
            if params.get("id", ""):
                data = GetTrackDetails(params.get("id", "")), "Trackinfo"
        elif info == 'albumshouts':
            if params["artistname"] and params["albumname"]:
                data = GetAlbumShouts(params["artistname"], params["albumname"]), "Shout"
        elif info == 'artistshouts':
            if params["artistname"]:
                data = GetArtistShouts(params["artistname"]), "Shout"
        elif info == 'topartists':
            data = GetTopArtists(), "TopArtists"
        elif info == 'hypedartists':
            data = GetHypedArtists(), "HypedArtists"
        elif info == 'latestdbmovies':
            data = get_db_movies('"sort": {"order": "descending", "method": "dateadded"}', params.get("limit", 10)), "LatestMovies"
        elif info == 'randomdbmovies':
            data = get_db_movies('"sort": {"method": "random"}', params.get("limit", 10)), "RandomMovies"
        elif info == 'inprogressdbmovies':
            method = '"sort": {"order": "descending", "method": "lastplayed"}, "filter": {"field": "inprogress", "operator": "true", "value": ""}'
            data = get_db_movies(method, params.get("limit", 10)), "RecommendedMovies"
    #  RottenTomatoesMovies
        elif info == 'intheaters':
            from RottenTomatoes import GetRottenTomatoesMovies
            data = GetRottenTomatoesMovies("movies/in_theaters"), "InTheatersMovies"
        elif info == 'boxoffice':
            from RottenTomatoes import GetRottenTomatoesMovies
            data = GetRottenTomatoesMovies("movies/box_office"), "BoxOffice"
        elif info == 'opening':
            from RottenTomatoes import GetRottenTomatoesMovies
            data = GetRottenTomatoesMovies("movies/opening"), "Opening"
        elif info == 'comingsoon':
            from RottenTomatoes import GetRottenTomatoesMovies
            data = GetRottenTomatoesMovies("movies/upcoming"), "ComingSoonMovies"
        elif info == 'toprentals':
            from RottenTomatoes import GetRottenTomatoesMovies
            data = GetRottenTomatoesMovies("dvds/top_rentals"), "TopRentals"
        elif info == 'currentdvdreleases':
            from RottenTomatoes import GetRottenTomatoesMovies
            data = GetRottenTomatoesMovies("dvds/current_releases"), "CurrentDVDs"
        elif info == 'newdvdreleases':
            from RottenTomatoes import GetRottenTomatoesMovies
            data = GetRottenTomatoesMovies("dvds/new_releases"), "NewDVDs"
        elif info == 'upcomingdvds':
            from RottenTomatoes import GetRottenTomatoesMovies
            data = GetRottenTomatoesMovies("dvds/upcoming"), "UpcomingDVDs"
        #  The MovieDB
        elif info == 'incinemas':
            data = GetMovieDBMovies("now_playing"), "InCinemasMovies"
        elif info == 'upcoming':
            data = GetMovieDBMovies("upcoming"), "UpcomingMovies"
        elif info == 'topratedmovies':
            data = GetMovieDBMovies("top_rated"), "TopRatedMovies"
        elif info == 'popularmovies':
            data = GetMovieDBMovies("popular"), "PopularMovies"
        elif info == 'airingtodaytvshows':
            data = GetMovieDBTVShows("airing_today"), "AiringTodayTVShows"
        elif info == 'onairtvshows':
            data = GetMovieDBTVShows("on_the_air"), "OnAirTVShows"
        elif info == 'topratedtvshows':
            data = GetMovieDBTVShows("top_rated"), "TopRatedTVShows"
        elif info == 'populartvshows':
            data = GetMovieDBTVShows("popular"), "PopularTVShows"
        elif info == 'similarmovies':
            dbid = params.get("dbid", False)
            if params.get("id", False):
                movie_id = params["id"]
            elif dbid and int(dbid) > 0:
                movie_id = GetImdbIDFromDatabase("movie", dbid)
                log("IMDB Id from local DB:" + str(movie_id))
            else:
                movie_id = ""
            if movie_id:
                data = GetSimilarMovies(movie_id), "SimilarMovies"
        elif info == 'similartvshows':
            tvshow_id = None
            dbid = params.get("dbid", False)
            name = params.get("name", False)
            tmdb_id = params.get("tmdb_id", False)
            tvdb_id = params.get("tvdb_id", False)
            imdb_id = params.get("imdb_id", False)
            if tmdb_id:
                tvshow_id = tmdb_id
            elif dbid and int(dbid) > 0:
                tvdb_id = GetImdbIDFromDatabase("tvshow", dbid)
                log("IMDB Id from local DB:" + str(tvdb_id))
                if tvdb_id:
                    tvshow_id = get_show_tmdb_id(tvdb_id)
                    log("tvdb_id to tmdb_id: %s --> %s" %
                        (str(tvdb_id), str(tvshow_id)))
            elif tvdb_id:
                tvshow_id = get_show_tmdb_id(tvdb_id)
                log("tvdb_id to tmdb_id: %s --> %s" %
                    (tvdb_id, str(tvshow_id)))
            elif imdb_id:
                tvshow_id = get_show_tmdb_id(imdb_id, "imdb_id")
                log("imdb_id to tmdb_id: %s --> %s" %
                    (imdb_id, str(tvshow_id)))
            elif name:
                tvshow_id = search_media(name, "", "tv")
                log("search string to tmdb_id: %s --> %s" %
                    (name, str(tvshow_id)))
            if tvshow_id:
                data = GetSimilarTVShows(tvshow_id), "SimilarTVShows"
        elif info == 'studio':
            if "studio" in params and params["studio"]:
                CompanyId = SearchforCompany(params["studio"])[0]["id"]
                data = GetCompanyInfo(CompanyId), "StudioInfo"
        elif info == 'set':
            if params.get("dbid", False) and "show" not in str(params.get("type", "")):
                name = GetMovieSetName(params["dbid"])
                if name:
                    params["setid"] = SearchForSet(name)
            if params.get("setid", False):
                SetData, info = GetSetMovies(params["setid"])
                if SetData:
                    data = SetData, "MovieSetItems"
        elif info == 'movielists':
            if params.get("dbid", False):
                movie_id = GetImdbIDFromDatabase("movie", params["dbid"])
                log("MovieDB Id:" + str(movie_id))
                if movie_id:
                    data = GetMovieLists(movie_id), "MovieLists"
        elif info == 'keywords':
            if params.get("dbid", False):
                movie_id = GetImdbIDFromDatabase("movie", params["dbid"])
                log("MovieDB Id:" + str(movie_id))
                if movie_id:
                    data = GetMovieKeywords(movie_id), "Keywords"
        elif info == 'popularpeople':
            data = GetPopularActorList(), "PopularPeople"
        elif info == 'extendedinfo':
            HOME.setProperty('infodialogs.active', "true")
            from DialogVideoInfo import DialogVideoInfo
            dialog = DialogVideoInfo(u'script-%s-DialogVideoInfo.xml' % ADDON_NAME, ADDON_PATH, id=params.get("id", ""),
                                     dbid=params.get("dbid", None), imdb_id=params.get("imdb_id", ""), name=params.get("name", ""))
            dialog.doModal()
            HOME.clearProperty('infodialogs.active')
        elif info == 'extendedactorinfo':
            HOME.setProperty('infodialogs.active', "true")
            from DialogActorInfo import DialogActorInfo
            dialog = DialogActorInfo(u'script-%s-DialogInfo.xml' % ADDON_NAME,
                                     ADDON_PATH, id=params.get("id", ""), name=params.get("name", ""))
            dialog.doModal()
            HOME.clearProperty('infodialogs.active')
        elif info == 'extendedtvinfo':
            HOME.setProperty('infodialogs.active', "true")
            from DialogTVShowInfo import DialogTVShowInfo
            dialog = DialogTVShowInfo(u'script-%s-DialogVideoInfo.xml' % ADDON_NAME, ADDON_PATH, id=params.get("id", ""),
                                      dbid=params.get("dbid", None), imdb_id=params.get("imdb_id", ""), name=params.get("name", ""))
            dialog.doModal()
            HOME.clearProperty('infodialogs.active')
        elif info == 'ratemedia':
            media_type = params.get("type", False)
            if media_type:
                if params.get("id", False) and params["id"]:
                    tmdb_id = params["id"]
                elif media_type == "movie":
                    tmdb_id = get_movie_tmdb_id(imdb_id=params.get("imdb_id", ""), dbid=params.get("dbid", ""), name=params.get("name", ""))
                elif media_type == "tv" and params["dbid"]:
                    tvdb_id = GetImdbIDFromDatabase("tvshow", params["dbid"])
                    tmdb_id = get_show_tmdb_id(tvdb_id=tvdb_id)
                # elif media_type == "episode" and params["dbid"]:
                #     tvdb_id = GetImdbIDFromDatabase("tvshow", params["dbid"])
                #     tmdb_id = get_show_tmdb_id(tvdb_id=tvdb_id)
                if tmdb_id:
                    rating = get_rating_from_user()
                    if rating:
                        send_rating_for_media_item(media_type, tmdb_id, rating)
        elif info == 'seasoninfo':
            if params.get("tvshow", False) and params.get("season", False):
                HOME.setProperty('infodialogs.active', "true")
                from DialogSeasonInfo import DialogSeasonInfo
                dialog = DialogSeasonInfo(u'script-%s-DialogVideoInfo.xml' % ADDON_NAME, ADDON_PATH, tvshow=params["tvshow"], season=params["season"])
                dialog.doModal()
                HOME.clearProperty('infodialogs.active')
            else:
                Notify("Error", "Required data missing in script call")
        elif info == 'directormovies':
            if params.get("director", False):
                director_id = GetPersonID(params["director"], skip_dialog=True)["id"]
                if director_id:
                    data = GetDirectorMovies(director_id), "DirectorMovies"
        elif info == 'writermovies':
            if params.get("writer", False) and not params["writer"].split(" / ")[0] == params.get("director", "").split(" / ")[0]:
                writer_id = GetPersonID(params["writer"], skip_dialog=True)["id"]
                if writer_id:
                    data = GetDirectorMovies(writer_id), "WriterMovies"
        elif info == 'similarmoviestrakt':
            if params.get("id", False) or params.get("dbid", False):
                if params.get("dbid", False):
                    movie_id = GetImdbIDFromDatabase("movie", params["dbid"])
                else:
                    movie_id = params.get("id", "")
                data = GetSimilarTrakt("movie", movie_id), "SimilarMovies"
        elif info == 'similartvshowstrakt':
            if (params.get("id", "") or params["dbid"]):
                if params.get("dbid", False):
                    if params.get("type") == "episode":
                        tvshow_id = get_tvshow_id_from_db_by_episode(params["dbid"])
                    else:
                        tvshow_id = GetImdbIDFromDatabase("tvshow", params["dbid"])
                else:
                    tvshow_id = params.get("id", "")
                data = GetSimilarTrakt("show", tvshow_id), "SimilarTVShows"
        elif info == 'airingshows':
            data = GetTraktCalendarShows("shows"), "AiringShows"
        elif info == 'premiereshows':
            data = GetTraktCalendarShows("premieres"), "PremiereShows"
        elif info == 'trendingshows':
            data = GetTrendingShows(), "TrendingShows"
        elif info == 'trendingmovies':
            data = GetTrendingMovies(), "TrendingMovies"
        elif info == 'similarartistsinlibrary':
            if params.get("artist_mbid"):
                data = GetSimilarArtistsInLibrary(params.get("artist_mbid")), "SimilarArtists"
        elif info == 'artistevents':
            if params.get("artist_mbid"):
                data = GetEvents(params.get("artist_mbid")), "ArtistEvents"
        elif info == 'youtubesearch':
            HOME.setProperty('%sSearchValue' % params.get("prefix", ""), params.get("id", ""))  # set properties
            if params.get("id", False):
                data = GetYoutubeSearchVideos(params.get("id", ""), params.get("hd", ""), params.get("orderby", "relevance")), "YoutubeSearch"
        elif info == 'youtubeplaylist':
            if params.get("id", False):
                data = GetYoutubePlaylistVideos(params.get("id", "")), "YoutubePlaylist"
        elif info == 'youtubeusersearch':
            user_name = params.get("id", "")
            if user_name:
                playlists = GetUserPlaylists(user_name)
                data = GetYoutubePlaylistVideos(playlists["uploads"]), "YoutubeUserSearch"
        elif info == 'nearevents':
            data = GetNearEvents(params.get("tag", ""), params.get("festivalsonly", ""), params.get("lat", ""), params.get("lon", ""), params.get("location", ""), params.get("distance", "")), "NearEvents"
        elif info == 'trackinfo':
            HOME.setProperty('%sSummary' % params.get("prefix", ""), "")  # set properties
            if params["artistname"] and params["trackname"]:
                TrackInfo = GetTrackInfo(params["artistname"], params["trackname"])
                HOME.setProperty('%sSummary' % params.get("prefix", ""), TrackInfo["summary"])  # set properties
        elif info == 'venueevents':
            if params["location"]:
                params["id"] = GetVenueID(params["location"])
            if params.get("id", ""):
                data = GetVenueEvents(params.get("id", "")), "VenueEvents"
            else:
                Notify("Error", "Could not find venue")
        elif info == 'topartistsnearevents':
            artists = GetXBMCArtists()
            from MiscScraper import GetArtistNearEvents
            data = GetArtistNearEvents(artists["result"]["artists"][0:49]), "TopArtistsNearEvents"
        # elif info == 'channels':
        #     channels = create_channel_list()
        elif info == 'favourites':
            if params.get("id", ""):
                favourites = GetFavouriteswithType(params.get("id", ""))
            else:
                favourites = GetFavourites()
                HOME.setProperty('favourite.count', str(len(favourites)))
                if len(favourites) > 0:
                    HOME.setProperty('favourite.1.name', favourites[-1]["Label"])
            data = favourites, "Favourites"
        elif info == 'similarlocal' and "dbid" in params:
            data = GetSimilarFromOwnLibrary(
                params["dbid"]), "SimilarLocalMovies"
        elif info == 'iconpanel':
            data = GetIconPanel(int(params["id"])), "IconPanel" + str(params["id"])
        elif info == 'weather':
            data = GetWeatherImages(), "WeatherImages"
        elif info == 'updatexbmcdatabasewithartistmbidbg':
            SetMusicBrainzIDsForAllArtists(False, False)
        elif info == 'setfocus':
            xbmc.executebuiltin("SetFocus(22222)")
        elif info == 'playliststats':
            GetPlaylistStats(params.get("id", ""))
        elif info == "sortletters":
            data = GetSortLetters(params["path"], params.get("id", "")), "SortLetters"
        elif info == 'slideshow':
            windowid = xbmcgui.getCurrentWindowId()
            Window = xbmcgui.Window(windowid)
            # focusid = Window.getFocusId()
            itemlist = Window.getFocus()
            numitems = itemlist.getSelectedPosition()
            log("items:" + str(numitems))
            for i in range(0, numitems):
                Notify(item.getProperty("Image"))
        elif info == 'action':
            xbmc.executebuiltin(params.get("id", ""))
        elif info == 'bounce':
            HOME.setProperty(params.get("name", ""), "True")
            xbmc.sleep(200)
            HOME.clearProperty(params.get("name", ""))
        elif info == "youtubevideo":
            if params.get("id", ""):
                xbmc.executebuiltin("Dialog.Close(all,true)")
                play_trailer(params.get("id", ""))
        elif info == 'playtrailer':
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            xbmc.sleep(500)
            if params.get("id", ""):
                movie_id = params.get("id", "")
            elif int(params.get("dbid", -1)) > 0:
                movie_id = GetImdbIDFromDatabase("movie", params["dbid"])
                log("MovieDBID from local DB:" + str(movie_id))
            elif params.get("imdb_id", ""):
                movie_id = get_movie_tmdb_id(params.get("imdb_id", ""))
            else:
                movie_id = ""
            if movie_id:
                trailer = GetTrailer(movie_id)
                xbmc.executebuiltin("Dialog.Close(busydialog)")
                if trailer:
                    play_trailer(trailer)
                else:
                    Notify("Error", "No Trailer available")
        elif info == 'updatexbmcdatabasewithartistmbid':
            SetMusicBrainzIDsForAllArtists(True, False)
        elif info == 'deletecache':
            HOME.clearProperties()
            for the_file in os.listdir(ADDON_DATA_PATH):
                file_path = os.path.join(ADDON_DATA_PATH, the_file)
                try:
                    if os.path.isfile(file_path) and not the_file == "settings.xml":
                        os.unlink(file_path)
                except Exception as e:
                    log(e)
            Notify("Cache deleted")
        elif info == 'syncwatchlist':
            pass
        if data:
            data, prefix = data
            passListToSkin(prefix, data, params.get("prefix", ""), params.get("window", ""), params.get("handle", ""), params.get("limit", 20))
