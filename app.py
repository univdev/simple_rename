import os
import re;

class SimpleRename:

    # Variables
    format_videos = ('.avi', '.mp4', '.mkv')
    format_subtitles = ('.smi', '.ass')

    videos = []
    subtitles = []

    dir = ""
    std_video_name = ""
    ep_start_char_cnt = None
    # ep_end_char_cnt = None

    # Methods
    def start(self):
        self.compare_files();
        self.select_std_video();
        self.change();

    def compare_files(self):
        for fname in os.listdir(self.dir):
            # video format regex
            reg_vid = '|'.join(self.format_videos)
            reg_subtitle = '|'.join(self.format_subtitles)

            if re.search('({})'.format(reg_vid), fname):
                self.videos.append(fname);
            if re.search('({})'.format(reg_subtitle), fname):
                self.subtitles.append(fname);

    def diff_get_cnt(self, std, str):
        for (idx, letter) in enumerate(std[:]):
            if letter != str[idx:idx+1]:
                return int(idx);

    def select_std_video(self):
        for fname in self.videos:
            # 제목 중 에피소드를 의미하는 글자의 위치를 구해오는 과정
            # add self.std_video_name
            if self.std_video_name == "":
                self.std_video_name = fname

            # 다른 영상 제목과 비교해서 서로 다른 글자가 시작되는 부분을 구함
            if self.ep_start_char_cnt is None and self.std_video_name is not "":
                self.ep_start_char_cnt = self.diff_get_cnt(self.std_video_name, fname);

                while self.ep_start_char_cnt is not None:
                    # 서로 다른 글자가 시작되는 부분이 에피소드의 첫 글자가 아닐 경우를 염두함. (01과 02를 비교했을 때의 경우 등)
                    letter = self.std_video_name[self.ep_start_char_cnt - 1: self.ep_start_char_cnt];
                    if letter != '0':
                        break;

                    self.ep_start_char_cnt -= 1;

    def change(self):
        for video in self.videos:
            start = self.ep_start_char_cnt;
            end = start + 1;
            episode = "";

            while True:
                if video[start:end].isdigit() is False:
                    break;
                episode = video[start:end];
                end += 1;

            for subtitle in self.subtitles:
                reg_video = '|'.join(self.format_videos);
                reg_subtitle = '|'.join(self.format_subtitles);
                subtitle_format = re.search('({})'.format(reg_subtitle), subtitle).group(0);

                print('({})'.format(episode), subtitle);

                # 현재 비디오와 일치하는 자막 파일을 찾으면 실행 됨.
                if re.search('({})'.format(episode), subtitle):
                    re_subtitle_name = re.sub('({})'.format(reg_video), subtitle_format, video);
                    os.rename(self.dir + "\\" + subtitle, self.dir + "\\" + re_subtitle_name);
                    break;
