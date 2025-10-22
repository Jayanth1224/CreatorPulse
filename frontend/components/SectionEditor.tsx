"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Edit3, 
  Save, 
  X, 
  Trash2, 
  ChevronDown,
  ChevronUp
} from "lucide-react";
import { NewsletterSection, getSectionIcon } from "@/lib/newsletter-parser";

interface SectionEditorProps {
  section: NewsletterSection;
  onUpdate: (sectionId: string, updates: Partial<NewsletterSection>) => void;
  onDelete: (sectionId: string) => void;
  onReorder: (sectionId: string, direction: 'up' | 'down') => void;
  canMoveUp: boolean;
  canMoveDown: boolean;
}

export function SectionEditor({
  section,
  onUpdate,
  onDelete,
  onReorder,
  canMoveUp,
  canMoveDown
}: SectionEditorProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [editTitle, setEditTitle] = useState(section.title);
  const [editContent, setEditContent] = useState(section.content);

  const handleSave = () => {
    onUpdate(section.id, {
      title: editTitle,
      content: editContent
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(section.title);
    setEditContent(section.content);
    setIsEditing(false);
  };


  const handleDelete = () => {
    if (confirm(`Are you sure you want to delete "${section.title}"?`)) {
      onDelete(section.id);
    }
  };

  return (
    <Card className="mb-4">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-lg">{getSectionIcon(section.type)}</span>
            {isEditing ? (
              <Input
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="font-semibold text-lg"
                placeholder="Section title"
              />
            ) : (
              <h3 className="font-semibold text-lg">{section.title}</h3>
            )}
            <Badge variant="secondary" className="text-xs">
              {section.type}
            </Badge>
          </div>
          
          <div className="flex items-center gap-2">
            {/* Reorder buttons */}
            <div className="flex flex-col gap-1">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onReorder(section.id, 'up')}
                disabled={!canMoveUp}
                className="h-6 w-6 p-0"
              >
                <ChevronUp className="h-3 w-3" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onReorder(section.id, 'down')}
                disabled={!canMoveDown}
                className="h-6 w-6 p-0"
              >
                <ChevronDown className="h-3 w-3" />
              </Button>
            </div>

            {/* Collapse/Expand */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="h-8 w-8 p-0"
            >
              {isCollapsed ? <ChevronDown className="h-4 w-4" /> : <ChevronUp className="h-4 w-4" />}
            </Button>

            {/* Action buttons */}
            {isEditing ? (
              <div className="flex gap-1">
                <Button size="sm" onClick={handleSave} className="h-8">
                  <Save className="h-3 w-3 mr-1" />
                  Save
                </Button>
                <Button size="sm" variant="outline" onClick={handleCancel} className="h-8">
                  <X className="h-3 w-3 mr-1" />
                  Cancel
                </Button>
              </div>
            ) : (
              <div className="flex gap-1">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setIsEditing(true)}
                  className="h-8"
                >
                  <Edit3 className="h-3 w-3 mr-1" />
                  Edit
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={handleDelete}
                  className="h-8 text-destructive hover:text-destructive"
                >
                  <Trash2 className="h-3 w-3 mr-1" />
                  Delete
                </Button>
              </div>
            )}
          </div>
        </div>
      </CardHeader>
      
      {!isCollapsed && (
        <CardContent>
          {isEditing ? (
            <div className="space-y-3">
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                className="w-full min-h-[200px] p-3 border border-border rounded-md bg-background text-foreground resize-y"
                placeholder="Section content..."
              />
            </div>
          ) : (
            <div 
              className="prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: section.content }}
            />
          )}
        </CardContent>
      )}
    </Card>
  );
}
