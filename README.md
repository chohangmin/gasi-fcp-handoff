# 가시제거연구소 Final Cut Pro 편집 인계

Mac에서 편집하고, 프로젝트 XML과 편집 기록은 Git으로 공유합니다. 기준은 30fps, 78.3667초의 V2.4입니다.

| 경로 | 내용 |
| --- | --- |
| `timeline/mackerel_v24_timeline.json` | 기준본 26컷의 원본 시간, 출력 위치, 줌, 오디오 큐 |
| `timeline/source_cuts.csv` | 초반 전환, 1·2입, 마지막 대화 등 후보 영상 8개의 원본 시간 |
| `timeline/v24_overlays.ass` | 기존 대사 자막과 게임 UI의 문구, 배치, 시간 |
| `graphics/` | 투명 카운터 0/5~5/5와 기존 엔딩 PNG |
| `tools/export_fcp_review.py` | 원본과 로컬 오디오에서 후보 클립을 다시 만드는 Python 스크립트 |

## Mac에서 처음 열기

1. Finder에서 `IMG_1083.MOV`와 `FCP_review_v25` 폴더를 Mac 또는 외장 SSD의 편집 폴더로 복사합니다.
2. Final Cut Pro에서 2160×3840, 30fps, Rec.709 프로젝트를 만든 뒤 MOV와 필요한 WAV·PNG를 가져옵니다.
3. `FCP_review_v25/mackerel_v24_brand_line_only.mp4`를 비교 영상으로 사용합니다. 4K 편집에는 `timeline/`의 원본 구간을 사용합니다. 카운터 PNG는 실제로 한 입 먹은 지점에서 교체합니다.
4. 기존 컷 길이를 유지할 때는 전체 수정 믹스를 타임라인 0초에 배치할 수 있습니다. 컷을 늘리면 그 지점 이후의 대사와 음악을 다시 맞춥니다. 02 대사 WAV는 기존 00:26.967의 브랜드 소개 컷 시작에 대응합니다.

현재 저장소에는 타임코드와 자막·그래픽이 있습니다. 첫 파이널컷 프로젝트를 만들면 **File → Export XML**에서 프로젝트를 내보내 `timeline/`에 버전 이름으로 저장합니다. 로컬 경로와 미디어 메타데이터가 포함될 수 있으므로 공개 저장소에 추가하기 전에 XML을 확인합니다.

진행 사항이나 오류를 공유할 때는 **프로젝트 버전, 출력 타임코드, 실제 상태, 원하는 결과**를 이슈에 적습니다. 영상이나 소리가 필요한 경우 해당 구간의 짧은 미리보기를 공유 폴더에서 연결합니다.

## 후보 클립을 다시 만들기

Python, Pillow, FFmpeg가 필요합니다. `Media/`에 촬영 원본, V2.4 기준 MP4, V2.4 클린 대사 WAV를 배치하면 아래 명령을 Windows에서 실행할 수 있습니다.

```sh
python tools/export_fcp_review.py --output FCP_review_v25
```

다른 위치의 파일은 `--source`, `--reference`, `--dialogue`로 지정합니다. Mac에서 스크립트를 실행하려면 설치된 모노스페이스 글꼴 경로를 `--font`로 지정합니다. 파이널컷에서 완성된 후보를 가져올 때는 Python이 필요 없습니다.
