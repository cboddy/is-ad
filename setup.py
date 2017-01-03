from setuptools import setup
setup(
        name="ad.finder",
        version="0.1",
        description="Text categorization: ad or no ad.",
        author="Chris Boddy",
        license="MIT",
        packages=["is_ad"],
        zip_safe=True,
        install_requires=[
            'numpy',
            'scipy',
            'scikit-learn'
        ],
        #url="",
        #entry_points={
        #    "console_scripts": ["rss-repo-server=rssrepo.server:main"],
        #    }
)
