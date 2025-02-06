public class Song {
    private String songName;
    private String songArtist;
    private int duration;

    public Song(String songName, String songArtist, int duration) {
        this.songName = songName;
        this.songArtist = songArtist;
        this.duration = duration;
    }

    public String getSongName() {
        return songName;
    }

    public String getSongArtist() {
        return songArtist;
    }

    public int getDuration() {
        return duration;
    }

}
