import java.util.ArrayList;
import java.util.List;

public class User {
    private String name;
    //private String status;-- if you want to add premium or free user
    private List<Playlist> playlists;

    public User(String name) {
        this.name = name;
        this.playlists=new ArrayList<>();
    }
    public Playlist createPlaylist(String name){
        Playlist playlist= new Playlist(name);
        playlists.add(playlist);
        return playlist;
    }
    public void addSong(Playlist playlist, Song song){
        if (!playlist.getSongs().contains(song)){
            playlist.addSong(song);
        }
    }
    public void searchSong(String query, List<Song> library) {
        for (Song song : library) {
            if (song.getSongName().contains(query)) {
                System.out.println("Found: " + song.getSongName());
            }
        }
    }
}

