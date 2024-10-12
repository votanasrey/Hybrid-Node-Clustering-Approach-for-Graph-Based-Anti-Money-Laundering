import React from "react";
import IcoMoon from "react-icomoon";
import IconSets from "./selection-icon-moon.json";

export type IIconName =
  | "add"
  | "arrow-down"
  | "arrow-left"
  | "arrow-right"
  | "arrow-up"
  | "bell"
  | "bookmark"
  | "calendar"
  | "camera"
  | "caret-down"
  | "caret-left"
  | "caret-right"
  | "caret-up"
  | "champion"
  | "chat"
  | "check"
  | "check-circle"
  | "chevron-down"
  | "chevron-left"
  | "chevron-right"
  | "chevron-up"
  | "clone"
  | "cocktail"
  | "cross"
  | "cross-circle"
  | "dashboard"
  | "dislike"
  | "expand"
  | "explore"
  | "export"
  | "eye-close"
  | "eye-open"
  | "file"
  | "filter"
  | "gift"
  | "hamburger"
  | "heart"
  | "home"
  | "info"
  | "like"
  | "login"
  | "logo-dark-bg"
  | "logo-light-bg"
  | "logout"
  | "map"
  | "marker"
  | "minus"
  | "moon"
  | "navigator"
  | "pencil"
  | "photo"
  | "pie-chart"
  | "script"
  | "search"
  | "settings"
  | "star"
  | "statistics"
  | "sun"
  | "time"
  | "trash"
  | "tree"
  | "upload"
  | "user";

interface IIconProps {
  icon: IIconName;
  size?: number;
  color?: string;
}

const Icon: React.FC<IIconProps> = ({ color, icon, size }) => {
  // console.log(Object.values(iconList(IconSets)).sort())
  return <IcoMoon icon={icon} iconSet={IconSets} color={color} size={size} />;
};

export default Icon;
