"use client";

import { useState, useEffect } from "react";
import { Navigation } from "@/components/layout/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { tonePresets } from "@/lib/mock-data";
import { Check, Mail, AlertCircle, Upload, Clock, Calendar, Settings, Plus, Trash2, Play } from "lucide-react";
import { SourceManager } from "@/components/SourceManager";
import { Source } from "@/types";
import {
  listAutoNewsletters,
  createAutoNewsletter,
  updateAutoNewsletter,
  deleteAutoNewsletter,
  generateAutoNewsletterNow,
  type AutoNewsletter,
  getBundles,
} from "@/lib/api-client";
import { ProtectedRoute } from "@/components/ProtectedRoute";

function SettingsPageContent() {
  const [activeSection, setActiveSection] = useState<string>("account");

  return (
    <>
      <Navigation />
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold mb-2">Settings</h1>
          <p className="text-muted">
            Manage your account, preferences, and integrations.
          </p>
        </div>

        <div className="grid lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <nav className="lg:col-span-1 space-y-1">
            <NavButton
              active={activeSection === "account"}
              onClick={() => setActiveSection("account")}
            >
              Account
            </NavButton>
            <NavButton
              active={activeSection === "esp"}
              onClick={() => setActiveSection("esp")}
            >
              Email Provider
            </NavButton>
            <NavButton
              active={activeSection === "recipients"}
              onClick={() => setActiveSection("recipients")}
            >
              Recipients
            </NavButton>
            <NavButton
              active={activeSection === "tone"}
              onClick={() => setActiveSection("tone")}
            >
              Tone & Voice
            </NavButton>
            <NavButton
              active={activeSection === "sources"}
              onClick={() => setActiveSection("sources")}
            >
              Content Sources
            </NavButton>
            <NavButton
              active={activeSection === "auto-newsletter"}
              onClick={() => setActiveSection("auto-newsletter")}
            >
              Auto Newsletter
            </NavButton>
            <NavButton
              active={activeSection === "billing"}
              onClick={() => setActiveSection("billing")}
            >
              Billing & Plan
            </NavButton>
          </nav>

          {/* Content */}
          <div className="lg:col-span-3 space-y-6">
            {activeSection === "account" && <AccountSection />}
            {activeSection === "esp" && <ESPSection />}
            {activeSection === "recipients" && <RecipientsSection />}
            {activeSection === "tone" && <ToneSection />}
            {activeSection === "sources" && <SourcesSection />}
            {activeSection === "auto-newsletter" && <AutoNewsletterSection />}
            {activeSection === "billing" && <BillingSection />}
          </div>
        </div>
      </main>
    </>
  );
}

export default function SettingsPage() {
  return (
    <ProtectedRoute>
      <SettingsPageContent />
    </ProtectedRoute>
  );
}

function NavButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
        active
          ? "bg-primary text-white"
          : "text-muted hover:bg-surface hover:text-foreground"
      }`}
    >
      {children}
    </button>
  );
}

function AccountSection() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Account Settings</CardTitle>
        <CardDescription>
          Manage your personal information and preferences
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="name">Full Name</Label>
          <Input
            id="name"
            defaultValue="Jayanth Bandi"
            className="mt-2"
          />
        </div>
        <div>
          <Label htmlFor="email">Email Address</Label>
          <Input
            id="email"
            type="email"
            defaultValue="jayanth@example.com"
            className="mt-2"
          />
        </div>
        <div>
          <Label htmlFor="timezone">Timezone</Label>
          <Select id="timezone" className="mt-2" defaultValue="America/Los_Angeles">
            <option value="America/Los_Angeles">Pacific Time (PT)</option>
            <option value="America/Denver">Mountain Time (MT)</option>
            <option value="America/Chicago">Central Time (CT)</option>
            <option value="America/New_York">Eastern Time (ET)</option>
            <option value="Europe/London">London (GMT)</option>
            <option value="Asia/Kolkata">India (IST)</option>
          </Select>
          <p className="text-xs text-muted mt-2">
            Used for scheduling draft delivery times
          </p>
        </div>
        <Button>Save Changes</Button>
      </CardContent>
    </Card>
  );
}

function ESPSection() {
  const [provider, setProvider] = useState<string>("sendgrid");
  const [isConnected, setIsConnected] = useState(false);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Email Service Provider</CardTitle>
        <CardDescription>
          Connect your email provider to send newsletters
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="provider">Provider</Label>
          <Select
            id="provider"
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
            className="mt-2"
          >
            <option value="sendgrid">SendGrid</option>
            <option value="mailgun">Mailgun</option>
            <option value="smtp">SMTP (Generic)</option>
          </Select>
        </div>

        {provider === "sendgrid" && (
          <div>
            <Label htmlFor="api-key">SendGrid API Key</Label>
            <Input
              id="api-key"
              type="password"
              placeholder="SG.xxxxxxxxxxxxxxxxxxxxx"
              className="mt-2"
            />
          </div>
        )}

        {provider === "mailgun" && (
          <>
            <div>
              <Label htmlFor="mailgun-domain">Domain</Label>
              <Input
                id="mailgun-domain"
                placeholder="mg.yourdomain.com"
                className="mt-2"
              />
            </div>
            <div>
              <Label htmlFor="mailgun-key">API Key</Label>
              <Input
                id="mailgun-key"
                type="password"
                placeholder="key-xxxxxxxxxxxxxxxxxxxxx"
                className="mt-2"
              />
            </div>
          </>
        )}

        {provider === "smtp" && (
          <>
            <div>
              <Label htmlFor="smtp-host">SMTP Host</Label>
              <Input
                id="smtp-host"
                placeholder="smtp.example.com"
                className="mt-2"
              />
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="smtp-port">Port</Label>
                <Input id="smtp-port" placeholder="587" className="mt-2" />
              </div>
              <div>
                <Label htmlFor="smtp-username">Username</Label>
                <Input id="smtp-username" placeholder="user@example.com" className="mt-2" />
              </div>
            </div>
            <div>
              <Label htmlFor="smtp-password">Password</Label>
              <Input
                id="smtp-password"
                type="password"
                placeholder="••••••••"
                className="mt-2"
              />
            </div>
          </>
        )}

        <div className="flex items-center gap-2">
          <Button onClick={() => setIsConnected(!isConnected)}>
            {isConnected ? "Disconnect" : "Connect & Verify"}
          </Button>
          {isConnected && (
            <Badge variant="success" className="flex items-center gap-1">
              <Check className="h-3 w-3" />
              Connected
            </Badge>
          )}
        </div>

        {isConnected && (
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4 flex items-start gap-3">
            <Mail className="h-5 w-5 text-green-600 dark:text-green-400 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-green-900 dark:text-green-100">
                Connection Verified
              </p>
              <p className="text-xs text-green-700 dark:text-green-300 mt-1">
                Your ESP is connected and ready to send newsletters.
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function RecipientsSection() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Default Recipient List</CardTitle>
        <CardDescription>
          Set your default recipient list for sending newsletters
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="recipient-list">Recipient Email or List</Label>
          <Input
            id="recipient-list"
            placeholder="newsletter@example.com"
            className="mt-2"
          />
          <p className="text-xs text-muted mt-2">
            Enter a single email address or your mailing list address
          </p>
        </div>
        <div>
          <Label htmlFor="from-name">From Name</Label>
          <Input
            id="from-name"
            placeholder="Your Name"
            defaultValue="Jayanth Bandi"
            className="mt-2"
          />
        </div>
        <div>
          <Label htmlFor="from-email">From Email</Label>
          <Input
            id="from-email"
            type="email"
            placeholder="you@example.com"
            defaultValue="jayanth@example.com"
            className="mt-2"
          />
        </div>
        <Button>Save Recipient Settings</Button>
      </CardContent>
    </Card>
  );
}

function ToneSection() {
  const [selectedTone, setSelectedTone] = useState("professional");

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Tone Preferences</CardTitle>
          <CardDescription>
            Choose your default writing tone for generated drafts
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid sm:grid-cols-2 gap-3">
            {tonePresets.map((preset) => (
              <button
                key={preset.value}
                onClick={() => setSelectedTone(preset.value)}
                className={`p-4 rounded-lg border-2 text-left transition-colors ${
                  selectedTone === preset.value
                    ? "border-primary bg-primary/5"
                    : "border-border hover:border-primary/50"
                }`}
              >
                <div className="font-semibold mb-1 flex items-center justify-between">
                  {preset.label}
                  {selectedTone === preset.value && (
                    <Check className="h-4 w-4 text-primary" />
                  )}
                </div>
                <div className="text-xs text-muted">{preset.description}</div>
              </button>
            ))}
          </div>
          <Button>Save Tone Preference</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Voice Training</CardTitle>
          <CardDescription>
            Upload samples of your writing to train a custom voice model
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer">
            <Upload className="h-8 w-8 text-muted mx-auto mb-3" />
            <p className="font-medium mb-1">Upload Writing Samples</p>
            <p className="text-xs text-muted mb-3">
              Upload at least 20 examples of your best newsletters or articles
            </p>
            <Button variant="outline" size="sm">
              Choose Files
            </Button>
          </div>
          <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-yellow-900 dark:text-yellow-100">
                Pro Feature
              </p>
              <p className="text-xs text-yellow-700 dark:text-yellow-300 mt-1">
                Voice training is available on the Pro plan. Upgrade to create a custom voice model.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function BillingSection() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Current Plan</CardTitle>
          <CardDescription>
            You're currently on the Free plan
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-semibold text-lg">Free Plan</div>
                <div className="text-sm text-muted">1 topic bundle, basic summaries</div>
              </div>
              <Badge variant="secondary">Active</Badge>
            </div>
            <Button>Upgrade to Pro</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Available Plans</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="font-semibold">Pro Plan</div>
              <div className="text-2xl font-bold">$25<span className="text-sm text-muted">/mo</span></div>
            </div>
            <ul className="text-sm text-muted space-y-1 mb-4">
              <li>✓ Custom voice training</li>
              <li>✓ Advanced analytics</li>
              <li>✓ 3+ topic bundles</li>
              <li>✓ Priority support</li>
            </ul>
            <Button className="w-full">Upgrade Now</Button>
          </div>

          <div className="border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="font-semibold">Agency Plan</div>
              <div className="text-2xl font-bold">Custom</div>
            </div>
            <ul className="text-sm text-muted space-y-1 mb-4">
              <li>✓ Multi-newsletter support</li>
              <li>✓ Shared analytics</li>
              <li>✓ Unlimited bundles</li>
              <li>✓ Dedicated account manager</li>
            </ul>
            <Button variant="outline" className="w-full">Contact Sales</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function SourcesSection() {
  const [sources, setSources] = useState<Source[]>([
    {
      id: "1",
      type: "rss",
      value: "https://techcrunch.com/feed/",
      label: "TechCrunch"
    },
    {
      id: "2", 
      type: "twitter",
      value: "@elonmusk",
      label: "Elon Musk"
    },
    {
      id: "3",
      type: "youtube", 
      value: "UCBJycsmduvYEL83R_U4JriQ",
      label: "Marques Brownlee"
    }
  ]);

  const handleAddSource = (source: Omit<Source, 'id'>) => {
    const newSource: Source = {
      ...source,
      id: Date.now().toString()
    };
    setSources([...sources, newSource]);
  };

  const handleRemoveSource = (sourceId: string) => {
    setSources(sources.filter(s => s.id !== sourceId));
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Content Sources</CardTitle>
        <CardDescription>
          Manage your RSS feeds, Twitter handles, and YouTube channels for content aggregation
        </CardDescription>
      </CardHeader>
      <CardContent>
        <SourceManager
          sources={sources}
          onAddSource={handleAddSource}
          onRemoveSource={handleRemoveSource}
        />
      </CardContent>
    </Card>
  );
}

function AutoNewsletterSection() {
  const [autoNewsletters, setAutoNewsletters] = useState<AutoNewsletter[]>([]);
  const [bundles, setBundles] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newNewsletter, setNewNewsletter] = useState({
    bundleId: "",
    scheduleTime: "08:00:00",
    scheduleFrequency: "daily",
    scheduleDay: null as number | null,
    emailRecipients: [""]
  });

  // Load from API
  useEffect(() => {
    (async () => {
      setLoading(true);
      console.log('Loading auto-newsletters and bundles...');
      try {
        const [newslettersRes, bundlesRes] = await Promise.all([
          listAutoNewsletters(),
          getBundles()
        ]);
        console.log('Newsletters response:', newslettersRes);
        console.log('Bundles response:', bundlesRes);
        
        // Handle newsletters response
        if (newslettersRes.error) {
          console.error('Newsletters API error:', newslettersRes.error);
          setAutoNewsletters([]);
        } else if (newslettersRes.data) {
          setAutoNewsletters(newslettersRes.data);
        } else {
          console.warn('No newsletters data received');
          setAutoNewsletters([]);
        }
        
        // Handle bundles response
        if (bundlesRes.error) {
          console.error('Bundles API error:', bundlesRes.error);
          setBundles([]);
        } else if (bundlesRes.data) {
          const bundlesArray = Array.isArray(bundlesRes.data) ? bundlesRes.data : [];
          console.log('Setting bundles:', bundlesArray);
          setBundles(bundlesArray);
        } else {
          console.warn('No bundles data received');
          setBundles([]);
        }
      } catch (error) {
        console.error('Error loading data:', error);
        setBundles([]);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleCreateNewsletter = async () => {
    if (!newNewsletter.bundleId) {
      alert("Select a content bundle");
      return;
    }
    setLoading(true);
    console.log('Creating auto-newsletter with data:', {
      bundle_id: newNewsletter.bundleId,
      schedule_time: newNewsletter.scheduleTime,
      schedule_frequency: newNewsletter.scheduleFrequency,
      schedule_day: newNewsletter.scheduleDay,
      email_recipients: newNewsletter.emailRecipients.filter(e => e.trim())
    });
    const res = await createAutoNewsletter({
      bundle_id: newNewsletter.bundleId,
      schedule_time: newNewsletter.scheduleTime,
      schedule_frequency: newNewsletter.scheduleFrequency as any,
      schedule_day: newNewsletter.scheduleDay,
      email_recipients: newNewsletter.emailRecipients.filter(e => e.trim())
    });
    console.log('API Response:', res);
    setLoading(false);
    if (res.error) {
      console.error('Error creating auto-newsletter:', res.error);
      alert(`Failed to create auto-newsletter: ${res.error.detail || JSON.stringify(res.error)}`);
      return;
    }
    setShowCreateForm(false);
    setNewNewsletter({ bundleId: "", scheduleTime: "08:00:00", scheduleFrequency: "daily", scheduleDay: null, emailRecipients: [""] });
    
    // Reload the list
    try {
      const list = await listAutoNewsletters();
      if (list.error) {
        console.error('Error reloading newsletters:', list.error);
        setAutoNewsletters([]);
      } else if (list.data) {
        setAutoNewsletters(list.data);
      } else {
        setAutoNewsletters([]);
      }
    } catch (error) {
      console.error('Error reloading newsletters:', error);
      setAutoNewsletters([]);
    }
  };

  const handleToggleActive = async (id: string, current: boolean) => {
    await updateAutoNewsletter(id, { is_active: !current });
    try {
      const list = await listAutoNewsletters();
      if (list.error) {
        console.error('Error reloading newsletters:', list.error);
        setAutoNewsletters([]);
      } else if (list.data) {
        setAutoNewsletters(list.data);
      } else {
        setAutoNewsletters([]);
      }
    } catch (error) {
      console.error('Error reloading newsletters:', error);
      setAutoNewsletters([]);
    }
  };

  const handleDeleteNewsletter = async (id: string) => {
    if (!confirm("Delete this auto newsletter?")) return;
    await deleteAutoNewsletter(id);
    try {
      const list = await listAutoNewsletters();
      if (list.error) {
        console.error('Error reloading newsletters:', list.error);
        setAutoNewsletters([]);
      } else if (list.data) {
        setAutoNewsletters(list.data);
      } else {
        setAutoNewsletters([]);
      }
    } catch (error) {
      console.error('Error reloading newsletters:', error);
      setAutoNewsletters([]);
    }
  };

  const handleGenerateNow = async (id: string) => {
    setLoading(true);
    const res = await generateAutoNewsletterNow(id);
    setLoading(false);
    if (res.error) {
      alert(res.error.detail);
    } else {
      alert("Generated and emailed. Check your inbox.");
    }
  };

  const formatLastGenerated = (dateString: string | null) => {
    if (!dateString) return "Never";
    const date = new Date(dateString);
    return date.toLocaleDateString() + " at " + date.toLocaleTimeString();
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            Auto Newsletter
          </CardTitle>
          <CardDescription>
            Set up automated newsletter generation and delivery. Get fresh newsletters delivered to your email automatically.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {(!autoNewsletters || autoNewsletters.length === 0) ? (
              <div className="text-center py-8">
                <Calendar className="h-12 w-12 text-muted mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">No Auto Newsletters</h3>
                <p className="text-muted mb-4">
                  Create your first auto-newsletter to get started with automated content generation.
                </p>
                <Button onClick={() => setShowCreateForm(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Create Auto Newsletter
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {autoNewsletters.map((newsletter) => (
                  <div key={newsletter.id} className="border border-border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="flex items-center gap-2">
                          <Clock className="h-4 w-4 text-muted" />
                          <span className="font-medium">{newsletter.bundle_id}</span>
                        </div>
                        <Badge variant={newsletter.is_active ? "success" : "secondary"}>
                          {newsletter.is_active ? "Active" : "Inactive"}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleToggleActive(newsletter.id, newsletter.is_active)}
                        >
                          <Settings className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDeleteNewsletter(newsletter.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleGenerateNow(newsletter.id)}
                        >
                          <Play className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-muted">Schedule:</span>
                        <span className="ml-2 font-medium">
                          {newsletter.schedule_frequency} at {newsletter.schedule_time}
                          {newsletter.schedule_day && ` (Day ${newsletter.schedule_day})`}
                        </span>
                      </div>
                      <div>
                        <span className="text-muted">Last Generated:</span>
                        <span className="ml-2 font-medium">
                          {formatLastGenerated(newsletter.last_generated || null)}
                        </span>
                      </div>
                      <div>
                        <span className="text-muted">Recipients:</span>
                        <span className="ml-2 font-medium">
                          {newsletter.email_recipients.length} email(s)
                        </span>
                      </div>
                      <div>
                        <span className="text-muted">Status:</span>
                        <span className="ml-2 font-medium">
                          {newsletter.is_active ? "Running" : "Paused"}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
                
                <Button onClick={() => setShowCreateForm(true)} className="w-full">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Another Auto Newsletter
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {showCreateForm && (
        <Card>
          <CardHeader>
            <CardTitle>Create Auto Newsletter</CardTitle>
            <CardDescription>
              Set up automated newsletter generation for your content bundle
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="bundle">Content Bundle</Label>
              <Select
                id="bundle"
                value={newNewsletter.bundleId}
                onChange={(e) => setNewNewsletter({...newNewsletter, bundleId: e.target.value})}
                className="mt-2"
              >
                <option value="">Select a bundle ({bundles.length} available)</option>
                {bundles.map(bundle => (
                  <option key={bundle.id} value={bundle.id}>{bundle.label || bundle.name}</option>
                ))}
              </Select>
              {bundles.length === 0 && (
                <p className="text-sm text-muted-foreground mt-1">
                  Loading bundles... If this persists, check browser console.
                </p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="schedule-time">Delivery Time (HH:MM:SS)</Label>
                <Input
                  id="schedule-time"
                  type="text"
                  value={newNewsletter.scheduleTime}
                  onChange={(e) => setNewNewsletter({...newNewsletter, scheduleTime: e.target.value})}
                  className="mt-2"
                />
              </div>
              <div>
                <Label htmlFor="frequency">Frequency</Label>
                <Select
                  id="frequency"
                  value={newNewsletter.scheduleFrequency}
                  onChange={(e) => setNewNewsletter({...newNewsletter, scheduleFrequency: e.target.value})}
                  className="mt-2"
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </Select>
              </div>
            </div>

            {(newNewsletter.scheduleFrequency === "weekly" || newNewsletter.scheduleFrequency === "monthly") && (
              <div>
                <Label htmlFor="schedule-day">
                  {newNewsletter.scheduleFrequency === "weekly" ? "Day of Week" : "Day of Month"}
                </Label>
                <Select
                  id="schedule-day"
                  value={newNewsletter.scheduleDay || ""}
                  onChange={(e) => setNewNewsletter({...newNewsletter, scheduleDay: parseInt(e.target.value)})}
                  className="mt-2"
                >
                  {newNewsletter.scheduleFrequency === "weekly" ? (
                    <>
                      <option value="1">Monday</option>
                      <option value="2">Tuesday</option>
                      <option value="3">Wednesday</option>
                      <option value="4">Thursday</option>
                      <option value="5">Friday</option>
                      <option value="6">Saturday</option>
                      <option value="7">Sunday</option>
                    </>
                  ) : (
                    Array.from({length: 31}, (_, i) => (
                      <option key={i+1} value={i+1}>{i+1}</option>
                    ))
                  )}
                </Select>
              </div>
            )}

            <div>
              <Label htmlFor="recipients">Email Recipients</Label>
              <div className="space-y-2 mt-2">
                {newNewsletter.emailRecipients.map((email, index) => (
                  <div key={index} className="flex gap-2">
                    <Input
                      type="email"
                      placeholder="recipient@example.com"
                      value={email}
                      onChange={(e) => {
                        const newRecipients = [...newNewsletter.emailRecipients];
                        newRecipients[index] = e.target.value;
                        setNewNewsletter({...newNewsletter, emailRecipients: newRecipients});
                      }}
                    />
                    {newNewsletter.emailRecipients.length > 1 && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          const newRecipients = newNewsletter.emailRecipients.filter((_, i) => i !== index);
                          setNewNewsletter({...newNewsletter, emailRecipients: newRecipients});
                        }}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ))}
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setNewNewsletter({
                    ...newNewsletter,
                    emailRecipients: [...newNewsletter.emailRecipients, ""]
                  })}
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Recipient
                </Button>
              </div>
            </div>

            <div className="flex gap-2">
              <Button onClick={handleCreateNewsletter}>
                Create Auto Newsletter
              </Button>
              <Button variant="outline" onClick={() => setShowCreateForm(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

