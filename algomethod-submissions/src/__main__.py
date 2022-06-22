import logging
import os
import typing

import algomethod
import selenium
import selext.webdriver

_LOGGER = logging.getLogger(__name__)

_LOGGING_FORMAT = "%(asctime)s %(levelname)s %(pathname)s %(message)s"
logging.basicConfig(
    format=_LOGGING_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S%z",
    handlers=[logging.StreamHandler()],
    level=logging.INFO,
)


ROOT_DIRECTORY = "com.algo-method"


# def _find_local_files() -> typing.List[str]:
#     return glob.glob(f"{ROOT_DIRECTORY}/**/*.*", recursive=True)


def fetch_all_submissions(
    driver: selenium.webdriver.Chrome,
) -> typing.Iterator[algomethod.Submission]:
    task_ids = algomethod.fetch_task_ids()
    for task_id in task_ids:
        print(task_id)
        submissions = algomethod.fetch_submissions(
            driver,
            task_id,
            "kagemeka",
        )
        for submission in submissions:
            yield submission


def _get_path(submission: algomethod.Submission) -> str:
    ext = algomethod.get_extension(submission.language)
    return f"{ROOT_DIRECTORY}/{submission.task_id}/{submission.id}.{ext}"


def _save_submission(submission: algomethod.Submission) -> None:
    import filesystem.path

    save_path = _get_path(submission)
    filesystem.path.prepare_directory(save_path)
    with open(save_path, mode="w") as f:
        f.write(submission.code)


def main() -> None:
    with selext.webdriver.create_chrome_driver(headless=True) as driver:
        submissions = fetch_all_submissions(driver)
        for submission in submissions:
            if os.path.exists(_get_path(submission)):
                continue
            try:
                submission.code = algomethod.fetch_submission_code(
                    driver,
                    submission.id,
                )
            except Exception as e:
                print(e)
                continue
            _save_submission(submission)


if __name__ == "__main__":
    main()
