# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
from telemetry.story import expectations


class SystemHealthDesktopCommonExpectations(expectations.StoryExpectations):
  def SetExpectations(self):
    self.DisableStory('browse:news:hackernews',
                      [expectations.ALL_WIN, expectations.ALL_MAC],
                      'crbug.com/676336')
    self.DisableStory('browse:search:google', [expectations.ALL_WIN],
                      'crbug.com/673775')
    self.DisableStory('play:media:google_play_music', [expectations.ALL],
                      'crbug.com/649392')
    self.DisableStory('play:media:soundcloud', [expectations.ALL_WIN],
                      'crbug.com/649392')
    self.DisableStory('play:media:pandora', [expectations.ALL],
                      'crbug.com/64939')
    self.DisableStory('browse:media:tumblr',
                      [expectations.ALL_WIN], 'crbug.com/773393')
    self.DisableStory('browse:news:cnn',
                      [expectations.ALL_MAC], 'crbug.com/728576')
    self.DisableStory('browse_accessibility:tools:gmail_compose',
                      [expectations.ALL], 'crbug.com/769809')
    self.DisableStory('browse:tools:maps', [expectations.ALL_MAC],
                      'crbug.com/773084')


class SystemHealthDesktopMemoryExpectations(expectations.StoryExpectations):
  def SetExpectations(self):
    self.DisableStory('browse:news:hackernews',
                      [expectations.ALL_WIN, expectations.ALL_MAC],
                      'crbug.com/676336')
    self.DisableStory('browse:search:google', [expectations.ALL_WIN],
                      'crbug.com/673775')
    self.DisableStory('load:games:miniclip', [expectations.ALL_MAC],
                      'crbug.com/664661')
    self.DisableStory('play:media:google_play_music', [expectations.ALL],
                      'crbug.com/649392')
    self.DisableStory('play:media:soundcloud', [expectations.ALL_WIN],
                      'crbug.com/649392')
    self.DisableStory('play:media:pandora', [expectations.ALL],
                      'crbug.com/64939')
    self.DisableStory('browse:news:cnn',
                      [expectations.ALL_MAC], 'crbug.com/728576')
    self.DisableStory('browse:social:twitter_infinite_scroll',
                      [expectations.ALL_WIN], 'crbug.com/728464')
    self.DisableStory('multitab:misc:typical24',
                      [expectations.ALL_MAC], 'crbug.com/742475')
    self.DisableStory('browse_accessibility:tools:gmail_compose',
                      [expectations.ALL], 'crbug.com/769809')
    self.DisableStory('browse:tools:maps', [expectations.ALL_MAC],
                      'crbug.com/773084')
    self.DisableStory('load:news:wikipedia',
                      [expectations.ALL_WIN], 'crbug.com/777931')
    self.DisableStory('load_accessibility:media:wikipedia',
                      [expectations.ALL_WIN], 'crbug.com/777931')


class SystemHealthMobileCommonExpectations(expectations.StoryExpectations):
  def SetExpectations(self):
    self.DisableStory('browse:shopping:flipkart', [expectations.ALL_ANDROID],
                      'crbug.com/708300')
    self.DisableStory('browse:news:globo', [expectations.ALL_ANDROID],
                      'crbug.com/714650')
    self.DisableStory('load:tools:gmail', [expectations.ALL_ANDROID],
                      'crbug.com/657433')
    self.DisableStory('browse:news:toi', [expectations.ALL_ANDROID],
                      'crbug.com/728081')
    self.DisableStory(
        'load:tools:drive',
        [expectations.ANDROID_NEXUS5X, expectations.ANDROID_WEBVIEW],
        'crbug.com/738854')
    # TODO(rnephew): This disabling should move to CanRunOnBrowser.
    self.DisableStory('browse:chrome:omnibox',
                      [expectations.ANDROID_WEBVIEW],
                      'Webview does not have omnibox')
    # TODO(rnephew): This disabling should move to CanRunOnBrowser.
    self.DisableStory('browse:chrome:newtab',
                      [expectations.ANDROID_WEBVIEW],
                      'Webview does not have NTP')
    # TODO(rnephew): This disabling should move to CanRunOnBrowser.
    self.DisableStory('long_running:tools:gmail-background',
                      [expectations.ANDROID_WEBVIEW],
                      'Webview does not have tabs')
    self.DisableStory('browse:shopping:avito',
                      [expectations.ANDROID_NEXUS6], 'crbug.com/736497')


class SystemHealthMobileMemoryExpectations(expectations.StoryExpectations):
  def SetExpectations(self):
    self.DisableStory('browse:shopping:flipkart', [expectations.ALL_ANDROID],
                      'crbug.com/708300')
    self.DisableStory('browse:news:globo', [expectations.ALL_ANDROID],
                      'crbug.com/714650')
    self.DisableStory('load:tools:gmail', [expectations.ALL_ANDROID],
                      'crbug.com/657433')
    self.DisableStory('browse:news:toi', [expectations.ALL_ANDROID],
                      'crbug.com/728081')
    self.DisableStory(
        'load:tools:drive',
        [expectations.ANDROID_NEXUS5X, expectations.ANDROID_WEBVIEW],
        'crbug.com/738854')
    self.DisableStory('long_running:tools:gmail-background',
                      [expectations.ANDROID_SVELTE], 'crbug.com/777355')
    # TODO(rnephew): This disabling should move to CanRunOnBrowser.
    self.DisableStory('browse:chrome:omnibox',
                      [expectations.ANDROID_WEBVIEW],
                      'Webview does not have omnibox')
    # TODO(rnephew): This disabling should move to CanRunOnBrowser.
    self.DisableStory('browse:chrome:newtab',
                      [expectations.ANDROID_WEBVIEW],
                      'Webview does not have NTP')
    # TODO(rnephew): This disabling should move to CanRunOnBrowser.
    self.DisableStory('long_running:tools:gmail-background',
                      [expectations.ANDROID_WEBVIEW],
                      'Webview does not have tabs')


class SystemHealthWebviewStartupExpectations(expectations.StoryExpectations):
  def SetExpectations(self):
    pass
