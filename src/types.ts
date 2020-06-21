export interface IComment {
  id: number;
  text: string;
  posted_at: Date;
}

export interface IRecipe {
  id: number;
  url: string;
  votes: number;
  comments: Array<IComment>;
}

export interface ICategory {
  name: string;
  recipes: Array<IRecipe>;
}
