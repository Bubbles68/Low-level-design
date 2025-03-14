import java.util.ArrayList;
import java.util.List;

public class Playlist {
    private String name;
    private List<Song> songs;

    public Playlist(String name) {
        this.name = name;
        this.songs = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public List<Song> getSongs() {
        return songs;
    }

    public void addSong(Song song){
        if (!songs.contains(song)) {
            songs.add(song);
        }
    }
    public void deleteSong(Song song){
        if (songs.contains(song)){
            songs.remove(song);
        }
        else{
            throw new NullPointerException("Song is not present in the playlist");
        }
    }
}
